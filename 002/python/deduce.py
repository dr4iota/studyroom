#!/usr/bin/env python3
"""Study 002: how far can a model deduce the possible outcomes of a concurrent I/O trace?

Everything is in this one file: the problem model, the generator, two exact solvers that
check each other, the natural-language rendering, model runs through the Claude Code CLI,
grading and the report. The problem is defined in ../premise.md.

Commands (run from this directory):
    python3 deduce.py gen  [--threads N --ops N --blocks N --values N --syncs N ...]
    python3 deduce.py show PROBLEM
    python3 deduce.py ask  PROBLEM --model M [--effort E] [--trial T]
    python3 deduce.py run  PROBLEM [--effort E] [--plan fable:1,opus:3,sonnet:3,haiku:3]
    python3 deduce.py regrade
    python3 deduce.py report
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import re
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent  # data lives at the study level: it is not Python-specific
PROBLEMS = STUDY / "problems"
ATTEMPTS = STUDY / "attempts"
PROMPTS = STUDY / "prompts"
PROMPT_VERSION = "v1"

THREADS = "ABCDEFGH"
BLOCKS = "xyzwuv"
SYNCS = "PQRSTUVW"
INIT = 0

DEFAULTS = {
    "threads": 2,        # N
    "ops": 3,            # max operations per thread; each thread gets ops-1 or ops
    "blocks": 1,         # M
    "values": 3,         # write constants are drawn from 1..values (repeats allowed)
    "syncs": 0,          # K sync points
    "relations": "pair,at",  # pair = before in one thread, after in another; at = barrier
    "p_read": 0.5,       # chance that an operation is a read
    "p_obs": 0.0,        # chance that a read's result is given
    "p_copy": 0.0,       # chance that a write copies an earlier unobserved read of its thread
    "min_given": 1,      # with p_obs > 0, at least this many reads have a given result
    "min_copies": 0,     # at least this many writes copy a read
    "min_pruned": 0,     # the asked locations rule out at least this many plausible rows
                         # (decoys + pruned, see traps())
    "adversarial": 0,    # 1: ask the locations whose answer holds the most traps (see traps());
                         # 2: the same for small answers, scored by score_few
    "mixed": 0,          # 1: keep only seeds where threads mix reads and writes, most start
                         #    with a write, and every block is written and used by two threads
    "max_queries": 3,    # asked locations: 1..max_queries
    "min_answers": 12,   # accepted size of the joint answer set
    "max_answers": 99,
}

# --------------------------------------------------------------------------- model
#
# A problem is a JSON-ready dict:
#   {"id", "seed", "params", "blocks": M, "syncs": K, "queries": [...],
#    "threads": [{"name": "A", "ops": [...], "events": [...]}]}
# An op is {"id": "A1", "kind": "read", "block": b, "obs": v or None}
#       or {"id": "A2", "kind": "write", "block": b, "data": int or the id of a read}.
# An event is {"slot": k, "rel": "before" | "after" | "at", "sync": h}. The thread's steps
# are start(op1), end(op1), start(op2), ...; slot k puts the event after k of them, so an
# odd slot falls inside an operation.
# A query is {"read": "A3"} (value returned) or {"final": b} (final content).


def flat_ops(p):
    return [op for th in p["threads"] for op in th["ops"]]


def thread_steps(th):
    """The thread's steps in program order: ("ev", event), ("start", op) or ("end", op)."""
    n = len(th["ops"])
    out = []
    for slot in range(2 * n + 1):
        out += [("ev", e) for e in th["events"] if e["slot"] == slot]
        if slot < 2 * n:
            out.append(("start" if slot % 2 == 0 else "end", th["ops"][slot // 2]))
    return out


def build_graph(p, effects):
    """The step poset as predecessor bitmasks.

    Node h < K is sync point h; an "at" event is that node itself. "before"/"after" events
    are nodes with an edge into/out of it. With ``effects``, each operation gets an extra
    node between its start and end: the instant it takes effect. ``info[i]`` is None or
    (kind, op) with kind in start/eff/end.
    """
    info = [None] * p["syncs"]
    edges = []

    def new(x):
        info.append(x)
        return len(info) - 1

    for th in p["threads"]:
        prev = None
        for kind, x in thread_steps(th):
            if kind == "ev":
                if x["rel"] == "at":
                    node = x["sync"]
                else:
                    node = new(None)
                    edges.append((node, x["sync"]) if x["rel"] == "before" else (x["sync"], node))
            else:
                node = new((kind, x))
                # The effect lies between start and end, unordered against events inside.
                if effects and kind == "start":
                    eff = new(("eff", x))
                    edges.append((node, eff))
                elif effects:
                    edges.append((eff, node))
            if prev is not None:
                edges.append((prev, node))
            prev = node
    preds = [0] * len(info)
    for a, b in edges:
        preds[b] |= 1 << a
    return preds, info


def topo_order(preds):
    """A topological order of the nodes, or None if the graph has a cycle."""
    order, done = [], 0
    pending = list(range(len(preds)))
    while pending:
        ready = [i for i in pending if preds[i] & ~done == 0]
        if not ready:
            return None
        for i in ready:
            order.append(i)
            done |= 1 << i
        pending = [i for i in pending if not done >> i & 1]
    return order


def apply(op, contents, vals, pos):
    """Take op's effect. ``vals[i]`` is the value read by op i. None if a given result fails."""
    b = op["block"]
    if op["kind"] == "read":
        x = contents[b]
        if op.get("obs") is not None and op["obs"] != x:
            return None
        i = pos[op["id"]]
        return contents, vals[:i] + (x,) + vals[i + 1:]
    d = op["data"]
    x = vals[pos[d]] if isinstance(d, str) else d
    return contents[:b] + (x,) + contents[b + 1:], vals


def project(queries, contents, vals, pos):
    return tuple(vals[pos[q["read"]]] if "read" in q else contents[q["final"]] for q in queries)


# --------------------------------------------------------------------------- solvers


def solve_brute(p, queries, limit=3_000_000):
    """Enumerator: every interleaving of every step, with an explicit effect step per
    operation, over the full step poset. States reached by different paths are merged."""
    preds, info = build_graph(p, effects=True)
    ops = flat_ops(p)
    pos = {op["id"]: i for i, op in enumerate(ops)}
    full = (1 << len(preds)) - 1
    out, seen = set(), set()
    stack = [(0, (INIT,) * p["blocks"], (None,) * len(ops))]
    while stack:
        st = stack.pop()
        if st in seen:
            continue
        seen.add(st)
        if len(seen) > limit:
            raise RuntimeError(f"brute: more than {limit} states")
        mask, contents, vals = st
        if mask == full:
            out.add(project(queries, contents, vals, pos))
            continue
        for i in range(len(preds)):
            if mask >> i & 1 or preds[i] & ~mask:
                continue
            c, v = contents, vals
            if info[i] is not None and info[i][0] == "eff":
                r = apply(info[i][1], c, v, pos)
                if r is None:
                    continue
                c, v = r
            stack.append((mask | 1 << i, c, v))
    return out, len(seen)


def action_order(p):
    """before[j]: bitmask of the operations that take effect before operation j in every
    execution, i.e. those whose end precedes j's start in the step poset."""
    preds, info = build_graph(p, effects=False)
    anc = [0] * len(preds)
    for x in topo_order(preds):
        for y in range(len(preds)):
            if preds[x] >> y & 1:
                anc[x] |= 1 << y | anc[y]
    ops = flat_ops(p)
    node = {(k, op["id"]): i for i, inf in enumerate(info) if inf for k, op in [inf]}
    before = []
    for b in ops:
        a_start = anc[node["start", b["id"]]]
        before.append(sum(1 << i for i, a in enumerate(ops) if a_start >> node["end", a["id"]] & 1))
    return before


def solve(p, queries):
    """Solver: effect orders are exactly the linear extensions of ``action_order``, so it
    runs over operations only, layer by layer, keeping a read's value only while a later
    copy or a query still needs it."""
    ops = flat_ops(p)
    n = len(ops)
    pos = {op["id"]: i for i, op in enumerate(ops)}
    before = action_order(p)
    asked = {pos[q["read"]] for q in queries if "read" in q}
    users = [0] * n
    for j, op in enumerate(ops):
        if op["kind"] == "write" and isinstance(op["data"], str):
            users[pos[op["data"]]] |= 1 << j
    layer = {(0, (INIT,) * p["blocks"], (None,) * n)}
    states = 1
    for _ in range(n):
        nxt = set()
        for mask, c, v in layer:
            for j in range(n):
                if mask >> j & 1 or before[j] & ~mask:
                    continue
                r = apply(ops[j], c, v, pos)
                if r is None:
                    continue
                m = mask | 1 << j
                v2 = tuple(x if i in asked or users[i] & ~m else None for i, x in enumerate(r[1]))
                nxt.add((m, r[0], v2))
        layer = nxt
        states += len(layer)
    return {project(queries, c, v, pos) for _, c, v in layer}, states


# --------------------------------------------------------------------------- traps


def copy_depths(p, queries):
    """For each answer combination, the fewest copy hops any execution needs to produce
    it. A constant or the initial 0 has depth 0; a copy has the depth of the read it copies
    plus one; a combination has the depth of its deepest value. Same walk as ``solve``,
    with every value tagged by its depth."""
    ops = flat_ops(p)
    n = len(ops)
    before = action_order(p)
    pos = {op["id"]: i for i, op in enumerate(ops)}
    asked = {pos[q["read"]] for q in queries if "read" in q}
    users = [0] * n
    for j, op in enumerate(ops):
        if op["kind"] == "write" and isinstance(op["data"], str):
            users[pos[op["data"]]] |= 1 << j
    layer = {(0, ((INIT, 0),) * p["blocks"], (None,) * n)}
    for _ in range(n):
        nxt = set()
        for mask, c, v in layer:
            for j in range(n):
                if mask >> j & 1 or before[j] & ~mask:
                    continue
                op, b = ops[j], ops[j]["block"]
                if op["kind"] == "read":
                    if op["obs"] is not None and op["obs"] != c[b][0]:
                        continue
                    v2, c2 = v[:j] + (c[b],) + v[j + 1:], c
                else:
                    d = op["data"]
                    x = (v[pos[d]][0], v[pos[d]][1] + 1) if isinstance(d, str) else (d, 0)
                    v2, c2 = v, c[:b] + (x,) + c[b + 1:]
                m = mask | 1 << j
                v2 = tuple(x if i in asked or users[i] & ~m else None for i, x in enumerate(v2))
                nxt.add((m, c2, v2))
        layer = nxt
    out = {}
    for _, c, v in layer:
        items = [v[pos[q["read"]]] if "read" in q else c[q["final"]] for q in queries]
        key, d = tuple(x[0] for x in items), max(x[1] for x in items)
        out[key] = min(out.get(key, d), d)
    return out


def outside_syncs(p):
    """The problem with every sync line inside an operation moved outside it, as if the
    whole operation were ordered by the line: "before" after its end, "after" before its
    start, "at" after its end. None if that makes the order cyclic."""
    q = json.loads(json.dumps(p))
    for th in q["threads"]:
        for e in th["events"]:
            if e["slot"] % 2:
                e["slot"] += -1 if e["rel"] == "after" else 1
        th["events"].sort(key=lambda e: e["slot"])
    return q if topo_order(build_graph(q, effects=False)[0]) is not None else None


def flow_candidates(p, queries):
    """Per asked location, the values that could reach it if order were ignored: for a
    block, 0 and the constants written to it, plus whatever its copies can carry; for a
    final value, only what is written to the block (0 if nothing is)."""
    ops = flat_ops(p)
    byid = {o["id"]: o for o in ops}
    reach = [{INIT} for _ in range(p["blocks"])]
    written = [set() for _ in range(p["blocks"])]
    changed = True
    while changed:
        changed = False
        for o in ops:
            if o["kind"] == "write":
                d = o["data"]
                vals = reach[byid[d]["block"]] if isinstance(d, str) else {d}
                if not vals <= reach[o["block"]] or not vals <= written[o["block"]]:
                    reach[o["block"]] |= vals
                    written[o["block"]] |= vals
                    changed = True
    return [sorted(reach[byid[q["read"]]["block"]]) if "read" in q else sorted(written[q["final"]] or {INIT})
            for q in queries]


def traps(p, queries, answers=None):
    """The combinations a reader is likely to get wrong, by kind:
    - interval: combinations that change when a sync line inside an operation is read as
      outside it (hidden true rows, or impossible rows that reading admits);
    - depth2, depth1: true rows needing at least 2 (exactly 1) copy hops;
    - decoys: impossible rows made of values each location can take on its own;
    - pruned: other impossible rows made of values that could reach each location if
      order were ignored (flow_candidates), so ruling them out takes the ordering.
    ``score`` weighs the first four by how often models got such rows wrong in the first
    610 runs (about 35%, 4.7%, 2.3% and 1.2% of row-runs, against 0.3% for other rows).
    ``score_few`` is for small answers: plausible rows that are ruled out count most."""
    answers = answers if answers is not None else solve(p, queries)[0]
    depths = copy_depths(p, queries)
    naive = outside_syncs(p)
    interval = set() if naive is None or naive == p else answers ^ solve(naive, queries)[0]
    marg = [sorted({r[i] for r in answers}) for i in range(len(queries))]
    decoys = set(itertools.product(*marg)) - answers
    kinds = {
        "interval": interval,
        "depth2": {k for k, d in depths.items() if d >= 2} - interval,
        "depth1": {k for k, d in depths.items() if d == 1} - interval,
        "decoys": decoys - interval,
    }
    kinds["pruned"] = set(itertools.product(*flow_candidates(p, queries))) - answers - decoys - interval
    out = {k: sorted(v) for k, v in kinds.items()}
    out["score"] = 10 * len(kinds["interval"]) + 2 * len(kinds["depth2"]) + len(kinds["depth1"]) \
        + len(kinds["decoys"]) // 2
    out["score_few"] = 10 * len(kinds["interval"]) + 4 * len(kinds["pruned"]) + 3 * len(kinds["decoys"]) \
        + 3 * len(kinds["depth2"]) + len(kinds["depth1"])
    return out


# --------------------------------------------------------------------------- generator


def well_mixed(threads, M):
    """Every thread both reads and writes, at least half start with a write, and every
    block is written and used by at least two threads."""
    if any(len({o["kind"] for o in th["ops"]}) < 2 for th in threads):
        return False
    if 2 * sum(th["ops"][0]["kind"] == "write" for th in threads) < len(threads):
        return False
    for b in range(M):
        users = [th for th in threads if any(o["block"] == b for o in th["ops"])]
        written = any(o["block"] == b and o["kind"] == "write" for th in threads for o in th["ops"])
        if len(users) < 2 or not written:
            return False
    return True


def generate(params, seed):
    """One problem from ``params`` and ``seed``, or None if this seed does not work out
    (cyclic sync, or no choice of queries gives an answer set of the wanted size)."""
    P = {**DEFAULTS, **params}
    rng = random.Random(seed)
    N, M = P["threads"], P["blocks"]
    observed = set()
    threads = []
    for t in range(N):
        name = THREADS[t]
        ops = []
        for k in range(rng.randint(max(1, P["ops"] - 1), P["ops"])):
            oid, b = f"{name}{k + 1}", rng.randrange(M)
            if rng.random() < P["p_read"]:
                ops.append({"id": oid, "kind": "read", "block": b, "obs": None})
                if rng.random() < P["p_obs"]:
                    observed.add(oid)
            else:
                srcs = [o["id"] for o in ops if o["kind"] == "read" and o["id"] not in observed]
                data = rng.choice(srcs) if srcs and rng.random() < P["p_copy"] else rng.randint(1, P["values"])
                ops.append({"id": oid, "kind": "write", "block": b, "data": data})
        threads.append({"name": name, "ops": ops, "events": []})

    rels = [r for r in P["relations"].split(",") if r]
    for h in range(P["syncs"]):
        if rng.choice(rels) == "pair":
            i, j = rng.sample(range(N), 2)
            marks = [(i, "before"), (j, "after")]
        else:
            marks = [(t, "at") for t in rng.sample(range(N), rng.randint(2, N))]
        for t, rel in marks:
            th = threads[t]
            th["events"].append({"slot": rng.randint(0, 2 * len(th["ops"])), "rel": rel, "sync": h})
    for th in threads:
        th["events"].sort(key=lambda e: e["slot"])

    if sum(isinstance(o.get("data"), str) for th in threads for o in th["ops"]) < P["min_copies"]:
        return None
    if P["mixed"] and not well_mixed(threads, M):
        return None
    p = {"seed": seed, "params": P, "blocks": M, "syncs": P["syncs"], "threads": threads, "queries": []}
    preds, info = build_graph(p, effects=True)
    if topo_order(preds) is None:
        return None

    # Given results come from one random execution, so the problem always has a solution.
    ops = flat_ops(p)
    pos = {op["id"]: i for i, op in enumerate(ops)}
    mask, c, v = 0, (INIT,) * M, (None,) * len(ops)
    while mask != (1 << len(preds)) - 1:
        i = rng.choice([i for i in range(len(preds)) if not mask >> i & 1 and preds[i] & ~mask == 0])
        mask |= 1 << i
        if info[i] is not None and info[i][0] == "eff":
            c, v = apply(info[i][1], c, v, pos)
    for op in ops:
        if op["id"] in observed:
            op["obs"] = v[pos[op["id"]]]
    if P["p_obs"] and len(observed) < P["min_given"]:
        return None

    cands = [{"read": op["id"]} for op in ops if op["kind"] == "read" and op["obs"] is None]
    cands += [{"final": b} for b in range(M)]
    subsets = [list(s) for k in range(1, P["max_queries"] + 1)
               for s in itertools.combinations(cands, k)]
    rng.shuffle(subsets)
    best = None
    for qs in subsets:
        ans = solve(p, qs)[0]
        if not P["min_answers"] <= len(ans) <= P["max_answers"]:
            continue
        if not P["adversarial"]:
            p["queries"] = qs
            return p
        score = traps(p, qs, ans)["score" if P["adversarial"] == 1 else "score_few"]
        if score and (best is None or score > best[0]):
            best = (score, qs)
    if best is None:
        return None
    p["queries"] = best[1]
    if P["min_pruned"]:
        t = traps(p, best[1])
        if len(t["decoys"]) + len(t["pruned"]) < P["min_pruned"]:
            return None
    return p


# --------------------------------------------------------------------------- rendering


def describe(op):
    blk = BLOCKS[op["block"]]
    if op["kind"] == "read":
        return f"read {blk}" + (f", returned {op['obs']}" if op["obs"] is not None else "")
    d = op["data"]
    return f"write the value read by {d} to {blk}" if isinstance(d, str) else f"write {d} to {blk}"


def describe_query(q):
    return f"the value returned by {q['read']}" if "read" in q else f"the final value of {BLOCKS[q['final']]}"


def render(p):
    """The problem instance in plain text, as the model sees it."""
    lines = [f"Blocks: {', '.join(BLOCKS[:p['blocks']])}."]
    if p["syncs"]:
        lines.append(f"Sync points: {', '.join(SYNCS[:p['syncs']])}.")
    for th in p["threads"]:
        lines.append(f"Thread {th['name']}:")
        split = {th["ops"][e["slot"] // 2]["id"] for e in th["events"] if e["slot"] % 2}
        for kind, x in thread_steps(th):
            if kind == "ev":
                lines.append(f"  -- {x['rel']} {SYNCS[x['sync']]}")
            elif kind == "start":
                lines.append(f"  {x['id']}{' starts' if x['id'] in split else ''}: {describe(x)}")
            elif x["id"] in split:
                lines.append(f"  {x['id']} ends")
    lines.append("Asked:")
    lines += [f"  Q{k + 1}: {describe_query(q)}" for k, q in enumerate(p["queries"])]
    return "\n".join(lines)


def make_prompt(p):
    return (PROMPTS / f"{PROMPT_VERSION}.md").read_text().replace("{instance}", render(p))


# --------------------------------------------------------------------------- grading


def parse_answer(text, arity):
    """The rows of the last BEGIN ... END block, and the lines that could not be read."""
    blocks = re.findall(r"^\W*BEGIN\W*$(.*?)^\W*END\W*$", text, re.M | re.S)
    if not blocks:
        return None, []
    rows, bad = set(), []
    for line in blocks[-1].splitlines():
        if not line.strip(" `\t"):
            continue
        nums = re.findall(r"-?\d+", line)
        if len(nums) == arity:
            rows.add(tuple(map(int, nums)))
        else:
            bad.append(line)
    return rows, bad


def grade(p, truth, text):
    rows, bad = parse_answer(text, len(p["queries"]))
    t = {tuple(r) for r in truth["answers"]}
    if rows is None:
        return {"parsed": False, "exact": False, "truth": len(t), "answered": 0,
                "missing": len(t), "extra": 0, "jaccard": 0.0, "bad_lines": []}
    return {
        "parsed": True,
        "exact": rows == t and not bad,
        "truth": len(t),
        "answered": len(rows),
        "missing": len(t - rows),
        "extra": len(rows - t),
        "jaccard": round(len(t & rows) / len(t | rows), 3) if t | rows else 1.0,
        "missing_rows": sorted(t - rows),
        "extra_rows": sorted(rows - t),
        "bad_lines": bad,
        **trap_hits(truth, t, rows),
    }


def trap_hits(truth, t, rows):
    """For each trap kind, how many of its rows the answer got wrong (missed when true,
    listed when impossible)."""
    if "traps" not in truth:
        return {}
    wrong = t ^ rows
    return {"trap_wrong": {k: len({tuple(r) for r in v} & wrong)
                           for k, v in truth["traps"].items() if not k.startswith("score")}}


# --------------------------------------------------------------------------- storage


def load(pid):
    d = PROBLEMS / pid
    return json.loads((d / "problem.json").read_text()), json.loads((d / "truth.json").read_text())


def dump(path, obj):
    path.write_text(json.dumps(obj, indent=1) + "\n")


def git_commit():
    r = subprocess.run(["git", "describe", "--always", "--dirty"], cwd=HERE, capture_output=True, text=True)
    return r.stdout.strip()


def param_prefix(P):
    """t<N>op<ops>b<M>v<V>[s<K>[p|a]][g<p_obs>][c<p_copy>][r<p_read>][x|x2][q<max_queries>]
    [a<min_answers>_<max_answers>], the probabilities
    in tenths; zero or default fields are left out. A problem is named <prefix>-<case>,
    with case 01, 02, ... per prefix; its seed is in problem.json. Selection rules
    (min_given, min_copies, min_pruned, mixed) only reject seeds, so they are not in the name;
    ``adversarial`` changes which locations are asked, so it is (x)."""
    P = {**DEFAULTS, **P}
    s = f"t{P['threads']}op{P['ops']}b{P['blocks']}v{P['values']}"
    if P["syncs"]:
        rels = set(P["relations"].split(","))
        s += f"s{P['syncs']}" + ("" if rels == {"pair", "at"} else "p" if rels == {"pair"} else "a")
    for key, letter in (("p_obs", "g"), ("p_copy", "c")):
        if P[key]:
            s += f"{letter}{round(P[key] * 10)}"
    if P["p_read"] != DEFAULTS["p_read"]:
        s += f"r{round(P['p_read'] * 10)}"
    if P["adversarial"]:
        s += "x" if P["adversarial"] == 1 else f"x{P['adversarial']}"
    if P["max_queries"] != DEFAULTS["max_queries"]:
        s += f"q{P['max_queries']}"
    if (P["min_answers"], P["max_answers"]) != (DEFAULTS["min_answers"], DEFAULTS["max_answers"]):
        s += f"a{P['min_answers']}_{P['max_answers']}"
    return s


def cases(prefix):
    """The existing problems with this parameter prefix."""
    return sorted(PROBLEMS.glob(f"{prefix}-[0-9][0-9]")) if PROBLEMS.exists() else []


def sort_key(pd):
    """Report order: by size and features, then seed."""
    P = json.loads((pd / "problem.json").read_text())
    P, seed = P["params"], P["seed"]
    return (P["threads"], P["syncs"], P["ops"], P["blocks"], P["p_obs"], P["p_copy"], seed)


def cmd_gen(a):
    params = {k: getattr(a, k) for k in DEFAULTS if getattr(a, k) is not None}
    prefix = param_prefix({**DEFAULTS, **params})
    done = cases(prefix)
    # Each parameter set starts from its own seed, so neighbouring sets do not share
    # skeletons; a new case continues after the seeds its earlier cases used.
    first = a.seed if a.seed is not None else int(hashlib.sha256(prefix.encode()).hexdigest()[:8], 16)
    start = max([first] + [json.loads((d / "problem.json").read_text())["seed"] + 1 for d in done])
    for seed in range(start, start + a.tries):
        p = generate(params, seed)
        if p:
            break
    else:
        sys.exit(f"no problem found in seeds {start}..{start + a.tries - 1}")
    pid = a.id or f"{prefix}-{len(done) + 1:02d}"
    if (PROBLEMS / pid).exists():
        sys.exit(f"{pid} exists")
    p = {"id": pid, **p}
    q = p["queries"]
    t0 = time.time()
    ans, s_states = solve(p, q)
    t1 = time.time()
    try:
        bans, b_states = solve_brute(p, q)
    except RuntimeError as e:
        bans, b_states = None, str(e)
    t2 = time.time()
    truth = {
        "answers": sorted(ans),
        "size": len(ans),
        "solver": {"states": s_states, "seconds": round(t1 - t0, 3)},
        "brute": {"states": b_states, "seconds": round(t2 - t1, 3),
                  "answers": None if bans is None else sorted(bans)},
        "agree": None if bans is None else bans == ans,
        "traps": traps(p, q, ans),
    }
    d = PROBLEMS / pid
    d.mkdir(parents=True)
    dump(d / "problem.json", p)
    dump(d / "truth.json", truth)
    (d / "problem.txt").write_text(render(p) + "\n")
    print(render(p))
    print(f"\n{pid}: seed {p['seed']}, {len(ans)} answers; brute agrees: {truth['agree']}")
    if truth["agree"] is False:
        sys.exit("SOLVER AND BRUTE DISAGREE")


def cmd_show(a):
    p, truth = load(a.problem)
    print(make_prompt(p) if a.prompt else render(p))
    if a.answers:
        print("\n".join(" ".join(map(str, r)) for r in truth["answers"]))


def cmd_ask(a):
    print(ask(a.problem, a.model, a.effort, a.trial))


def ask(pid, model, effort, trial):
    p, truth = load(pid)
    d = ATTEMPTS / pid / f"{model}-{effort}-{trial}"
    if d.exists():
        return f"{d.relative_to(STUDY)}: exists, skipped"
    prompt = make_prompt(p)
    # One copy of the exact prompt per problem and prompt version, shared by all runs.
    pf = ATTEMPTS / pid / f"prompt-{PROMPT_VERSION}.txt"
    if pf.exists() and pf.read_text() != prompt:
        return f"{pf.relative_to(STUDY)}: differs from the prompt now built; not run"
    cmd = ["claude", "-p", "--model", model, "--effort", effort, "--tools", "",
           "--setting-sources", "", "--no-session-persistence",
           "--system-prompt", "Answer the user's question.", "--output-format", "json"]
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with tempfile.TemporaryDirectory() as cwd:  # empty, so no project files leak in
        r = subprocess.run(cmd, input=prompt, cwd=cwd, capture_output=True, text=True, timeout=3600)
    if r.returncode:
        return f"{pid} {model}-{effort}-{trial}: claude failed ({r.returncode}): {r.stderr[-500:]}"
    resp = json.loads(r.stdout)
    usage = resp.get("usage", {})
    d.mkdir(parents=True)
    if not pf.exists():
        pf.write_text(prompt)
    reply = resp.pop("result", "")  # kept in reply.md only
    dump(d / "response.json", resp)
    (d / "reply.md").write_text(reply)
    dump(d / "meta.json", {
        "problem": pid, "model": model, "model_id": ",".join(resp.get("modelUsage", {})),
        "effort": effort, "trial": trial, "prompt": PROMPT_VERSION, "harness": git_commit(),
        "started": started, "seconds": round(resp.get("duration_ms", 0) / 1000, 1),
        "cost_usd": resp.get("total_cost_usd"), "output_tokens": usage.get("output_tokens"),
        "thinking_tokens": usage.get("output_tokens_details", {}).get("thinking_tokens"),
    })
    g = grade(p, truth, reply)
    dump(d / "grade.json", g)
    verdict = "exact" if g["exact"] else f"-{g['missing']} +{g['extra']}" if g["parsed"] else "no answer"
    return f"{pid} {model}-{effort}-{trial}: {verdict} ({g['answered']}/{g['truth']})"


def cmd_run(a):
    jobs = [(m, t) for m, k in (x.split(":") for x in a.plan.split(",")) for t in range(1, int(k) + 1)]
    with ThreadPoolExecutor(a.parallel) as ex:
        for line in ex.map(lambda j: ask(a.problem, j[0], a.effort, j[1]), jobs):
            print(line, flush=True)


def cmd_regrade(a):
    """Add trap data to every truth.json that lacks it, and regrade every stored reply."""
    n = 0
    for pd in sorted(d for d in PROBLEMS.iterdir() if not d.name.startswith("_")):
        p, truth = load(pd.name)
        if "traps" not in truth:
            truth["traps"] = traps(p, p["queries"], {tuple(r) for r in truth["answers"]})
            dump(pd / "truth.json", truth)
        for d in sorted((ATTEMPTS / pd.name).glob("*/reply.md")) if (ATTEMPTS / pd.name).exists() else []:
            dump(d.parent / "grade.json", grade(p, truth, d.read_text()))
            n += 1
    print(f"regraded {n} replies")


def cmd_report(a):
    out = ["# Report", "", "Generated by `python3 deduce.py report`. A cell lists the trials: `✓` is an",
           "exact answer, `−m+e` means m possible combinations missed and e impossible ones",
           "listed, `∅` is no readable answer.", ""]
    trials = {}  # (problem, effort, model) -> [(trial, cell, exact)]
    for f in ATTEMPTS.glob("*/*/meta.json"):
        m, g = json.loads(f.read_text()), json.loads((f.parent / "grade.json").read_text())
        cell = "✓" if g["exact"] else f"−{g['missing']}+{g['extra']}" if g["parsed"] else "∅"
        trials.setdefault((m["problem"], m["effort"], m["model"]), []).append((m["trial"], cell, g["exact"]))
    order = ["fable", "opus", "sonnet", "haiku"]
    models = sorted({k[2] for k in trials}, key=lambda x: (order.index(x) if x in order else 99, x))
    efforts = sorted({k[1] for k in trials}, key=lambda e: ["low", "medium", "high", "xhigh", "max"].index(e))
    problems = sorted((d for d in PROBLEMS.iterdir() if not d.name.startswith("_")), key=sort_key)
    for effort in efforts:
        totals = {}
        for title, synced in (("no sync", False), ("with sync", True)):
            out += [f"## Effort {effort}, {title}", "", "| problem | answers | " + " | ".join(models) + " |",
                    "|---|---|" + "---|" * len(models)]
            for pd in problems:
                p = json.loads((pd / "problem.json").read_text())
                if bool(p["syncs"]) != synced:
                    continue
                cells = []
                for model in models:
                    ts = sorted(trials.get((pd.name, effort, model), []))
                    t = totals.setdefault((synced, model), [0, 0])
                    t[0] += sum(x for _, _, x in ts)
                    t[1] += len(ts)
                    cells.append(" ".join(c for _, c, _ in ts))
                size = json.loads((pd / "truth.json").read_text())["size"]
                out.append(f"| {pd.name} | {size} | " + " | ".join(cells) + " |")
            out.append("")
        out += [f"## Effort {effort}, exact answers / trials", "", "| model | no sync | with sync |",
                "|---|---|---|"]
        for model in models:
            out.append(f"| {model} | " + " | ".join("{}/{}".format(*totals.get((s, model), [0, 0]))
                                                   for s in (False, True)) + " |")
        out.append("")
    kinds = ["interval", "depth2", "depth1", "decoys", "pruned"]
    for effort in efforts:
        out += [f"## Effort {effort}, wrong rows by trap kind", "",
                "Rows a model got wrong (missed or impossible), and how many fall on each trap",
                "kind (premise.md §2).", "",
                "| model | wrong rows | " + " | ".join(kinds) + " | other |", "|---|---|" + "---|" * (len(kinds) + 1)]
        for model in models:
            w, k = 0, dict.fromkeys(kinds, 0)
            for f in ATTEMPTS.glob(f"*/{model}-{effort}-*/grade.json"):
                g = json.loads(f.read_text())
                if not g["parsed"] or "trap_wrong" not in g:
                    continue
                w += g["missing"] + g["extra"]
                for x in kinds:
                    k[x] += g["trap_wrong"].get(x, 0)
            out.append(f"| {model} | {w} | " + " | ".join(str(k[x]) for x in kinds) + f" | {w - sum(k.values())} |")
        out.append("")
    out += ["# Details", ""]
    for pd in problems:
        p, truth = load(pd.name)
        P = p["params"]
        nev = sum(len(th["events"]) for th in p["threads"])
        out += [f"## {pd.name}", "",
                f"N={P['threads']} ops≤{P['ops']} M={P['blocks']} values={P['values']} "
                f"syncs={P['syncs']} ({nev} events) p_obs={P['p_obs']} p_copy={P['p_copy']}; "
                f"{len(p['queries'])} asked, {truth['size']} answers, brute agrees: {truth['agree']}"
                + "".join(f"; selected: {k}={P[k]}" for k in ("min_given", "min_copies", "min_pruned", "mixed")
                          if P.get(k, 0) > 0 and (k != "min_given" or P["p_obs"])), ""]
        rows = {}
        for d in sorted((ATTEMPTS / pd.name).glob("*/meta.json")) if (ATTEMPTS / pd.name).exists() else []:
            d = d.parent
            m, g = json.loads((d / "meta.json").read_text()), json.loads((d / "grade.json").read_text())
            cell = "✓" if g["exact"] else f"-{g['missing']} +{g['extra']}" if g["parsed"] else "∅"
            rows.setdefault((m["model"], m["effort"]), []).append((m["trial"], cell, m["thinking_tokens"]))
        if rows:
            out += ["| model | effort | trials | thinking tokens |", "|---|---|---|---|"]
            for (model, effort), ts in sorted(rows.items()):
                ts.sort()
                out.append(f"| {model} | {effort} | {', '.join(c for _, c, _ in ts)} | "
                           f"{', '.join(str(k) for _, _, k in ts)} |")
            out.append("")
    (STUDY / "REPORT.md").write_text("\n".join(out))
    print("\n".join(out))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gen", help="generate a problem and its truth")
    for k, v in DEFAULTS.items():
        g.add_argument(f"--{k.replace('_', '-')}", dest=k, type=type(v), default=None)
    g.add_argument("--seed", type=int, help="first seed to try (default: derived from the parameters)")
    g.add_argument("--tries", type=int, default=200)
    g.add_argument("--id")
    s = sub.add_parser("show", help="print a problem")
    s.add_argument("problem")
    s.add_argument("--prompt", action="store_true", help="the whole prompt")
    s.add_argument("--answers", action="store_true")
    k = sub.add_parser("ask", help="one model run")
    k.add_argument("problem")
    k.add_argument("--model", required=True)
    k.add_argument("--effort", default="low")
    k.add_argument("--trial", type=int, default=1)
    r = sub.add_parser("run", help="the model plan on one problem")
    r.add_argument("problem")
    r.add_argument("--effort", default="low")
    r.add_argument("--plan", default="fable:1,opus:3,sonnet:3,haiku:3")
    r.add_argument("--parallel", type=int, default=2)
    sub.add_parser("regrade", help="add trap data to old problems and regrade all replies")
    sub.add_parser("report", help="write REPORT.md")
    a = ap.parse_args(argv)
    {"gen": cmd_gen, "show": cmd_show, "ask": cmd_ask, "run": cmd_run, "regrade": cmd_regrade, "report": cmd_report}[a.cmd](a)


if __name__ == "__main__":
    main()
