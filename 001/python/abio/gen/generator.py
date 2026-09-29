"""GEN: seeded random setups from hyperparameters (premise.md §4 GEN).

Procedure (one attempt; retried when random events make the poset cyclic):

1. Draw each thread's action kinds (``actions_per_thread`` + ``kind_mix``) and blocks
   (``block_skew``, ``writers_per_block``).
2. Interleave start and done steps per thread with at most ``max_in_flight`` actions in
   flight; completions happen in random order (asynchronous I/O).
3. Draw write/RCW contents with :mod:`abio.gen.exprgen` from reads already completed in
   the same thread; replace a fraction ``1 - p_w`` by ``"*"``.
4. Insert ``events_per_thread`` events per thread, at most one per (sync point,
   relation), ordered ``before < at < after`` per sync point within a thread.
5. Run one hidden full schedule (random linearization, random effect points) and
   reveal each read/RCW result with probability ``p_r``. Observations therefore come
   from a real run, so the setup is realizable.

Everything is drawn from ``random.Random(seed)``: the same hyperparameters give the same
setup, byte for byte.
"""

from __future__ import annotations

import random
from .. import terms as T
from ..lin.random_topo import random_linearization
from ..model import REL_RANK, MalformedSetup, Semantics, Setup, Step, Thread
from ..semantics import Schedule, execute, random_effects
from .exprgen import random_constant, random_expr, weighted_choice, zipf_weights
from .hyperparams import resolve

PREFIX = {"read": "r", "write": "w", "rcw": "c"}


def generate(hp: dict | None = None) -> tuple[Setup, Schedule]:
    """Return ``(setup, hidden_schedule)`` for a (partial) hyperparameter map."""
    hp = resolve(hp)
    rng = random.Random(hp["seed"])
    last: Exception | None = None
    for _ in range(hp["max_attempts"]):
        try:
            return _attempt(hp, rng)
        except MalformedSetup as ex:  # cyclic sync pattern; draw again
            last = ex
    raise RuntimeError(f"no well-formed setup in {hp['max_attempts']} attempts: {last}")


def _kinds(hp: dict, rng: random.Random) -> list[list[str]]:
    n = hp["threads"]
    apt = hp["actions_per_thread"]
    if isinstance(apt, int):
        return [[weighted_choice(rng, hp["kind_mix"]) for _ in range(apt)] for _ in range(n)]
    total = apt.get("total", apt)
    pool = [k for k, c in total.items() for _ in range(int(c))]
    rng.shuffle(pool)
    out: list[list[str]] = [[] for _ in range(n)]
    for k in pool:
        out[rng.randrange(n)].append(k)
    return out


def _attempt(hp: dict, rng: random.Random) -> tuple[Setup, Schedule]:
    M, K = hp["blocks"], hp["sync_points"]
    content, know = hp["content"], hp["knowledge"]
    pool, depth, classes = content["value_pool"], content["max_depth"], content["classes"]
    skew = hp["block_skew"]
    bweights = zipf_weights(M, skew.get("s", 1.0)) if skew.get("kind") == "zipf" else [1.0] * M
    cap = hp["writers_per_block"]
    writer_threads: list[set[int]] = [set() for _ in range(M)]
    counters = {"read": 0, "write": 0, "rcw": 0}

    threads = []
    for ti, kinds in enumerate(_kinds(hp, rng)):
        steps: list[Step] = []
        pending = list(kinds)
        in_flight: list[Step] = []
        completed_reads: list[str] = []
        while pending or in_flight:
            can_start = pending and len(in_flight) < hp["max_in_flight"]
            if can_start and (not in_flight or rng.random() < 0.5):
                kind = pending.pop(0)
                allowed = list(range(M))
                if kind != "read" and cap is not None:
                    allowed = [b for b in allowed if ti in writer_threads[b] or len(writer_threads[b]) < cap]
                    if not allowed:
                        kind, allowed = "read", list(range(M))
                block = rng.choices(allowed, [bweights[b] for b in allowed])[0]
                counters[kind] += 1
                aid = f"{PREFIX[kind]}{counters[kind]}"
                step = Step(kind, block, aid)
                if kind != "read":
                    writer_threads[block].add(ti)
                    step.data = random_expr(rng, completed_reads, classes, pool, depth)
                    if rng.random() >= know["p_w"]:
                        step.data = None
                if kind == "rcw":
                    step.expect = random_constant(rng, pool)
                steps.append(step)
                in_flight.append(step)
            else:
                s = in_flight.pop(rng.randrange(len(in_flight)))
                steps.append(Step("done", s.id))
                if s.kind == "read":
                    completed_reads.append(s.id)
        threads.append(Thread(f"t{ti}", _with_events(hp, rng, steps)))

    init = [random_constant(rng, pool) if rng.random() < know["init_known"] else T.Init(b) for b in range(M)]
    sem = Semantics(register=hp["semantics"].get("register", "atomic"), rcw_result=hp["semantics"].get("rcw_result", "old"))
    sid = hp["id"] or f"gen-{hp['seed']}"
    meta = {"tool": "abio gen", "seed": hp["seed"], "hyperparams": {k: v for k, v in hp.items() if k not in ("format", "version")}}
    setup = Setup(sid, M, K, init, threads, sem, meta)

    order = random_linearization(setup, rng)
    truth = execute(setup, order, random_effects(setup, order, rng))
    truth.meta = {"tool": "abio gen", "role": "truth"}
    if know["p_r"] > 0:
        flag = sem.rcw_result == "flag"
        for th in setup.threads:
            for s in th.steps:
                a = setup.actions.get(s.target) if s.kind == "done" else None
                if a is not None and a.returns and rng.random() < know["p_r"]:
                    v = truth.results[a.id]
                    if a.kind == "rcw" and flag:
                        v = "ok" if v == T.substitute(a.expect, lambda x: _value(setup, truth, x)) else "fail"
                    s.data = v
        setup = Setup.from_doc(setup.to_doc())  # re-derive observed results
    return setup, truth


def _value(setup: Setup, truth: Schedule, aid: str) -> T.Term:
    a = setup.actions[aid]
    if a.kind == "read":
        return truth.results[aid]
    return T.Unk(aid) if a.data is None else T.substitute(a.data, lambda x: _value(setup, truth, x))


def _with_events(hp: dict, rng: random.Random, steps: list[Step]) -> list[Step]:
    n_ev = hp["events_per_thread"]
    if not n_ev:
        return steps
    pairs = [(k, r) for k in range(hp["sync_points"]) for r in hp["relations"]]
    chosen = rng.sample(pairs, n_ev)
    slots = sorted(rng.randint(0, len(steps)) for _ in chosen)
    # Within one sync point, give earlier slots to earlier relations (before < at < after).
    by_k: dict[int, list[str]] = {}
    for k, r in chosen:
        by_k.setdefault(k, []).append(r)
    ks = [k for k, _ in chosen]
    rng.shuffle(ks)
    for rels in by_k.values():
        rels.sort(key=REL_RANK.__getitem__)
    events: list[tuple[int, Step]] = []
    for slot, k in zip(slots, ks):
        events.append((slot, Step(by_k[k].pop(0), k)))
    out: list[Step] = []
    ei = 0
    for i in range(len(steps) + 1):
        while ei < len(events) and events[ei][0] == i:
            out.append(events[ei][1])
            ei += 1
        if i < len(steps):
            out.append(steps[i])
    return out

