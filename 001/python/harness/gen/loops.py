"""Seeded random loop setups (``harness.loops``) for grading the loop tasks.

Each thread gets a prefix, a body and a suffix, each a small segment of reads and
writes, with up to ``max_in_flight`` actions open at once inside the segment. Data:

- **prefix:** constants, copies or combinations of earlier prefix reads;
- **body:** a constant, or a copy of one read: earlier in the same iteration, or in the
  prefix;
- **suffix:** constants, copies or combinations of prefix and suffix reads.

With ``sync``, bodies get per-iteration events (``loop_sync_points``), and prefixes and
suffixes may get plain events. Setups whose unrolled poset is cyclic, or that break a
loop rule, are drawn again.
"""

from __future__ import annotations

import random

from .. import terms as T
from ..loops import LoopSetup
from ..model import REL_RANK, MalformedSetup
from .exprgen import random_constant, random_expr


def _segment(rng, tid, seg, n_actions, blocks, mif, pool, counter, readable, classes):
    """Steps of one segment; ``readable``: reads already completed (refs allowed)."""
    steps, pending, open_, done_reads = [], n_actions, [], []
    while pending or open_:
        if pending and len(open_) < mif and (not open_ or rng.random() < 0.5):
            kind = "read" if rng.random() < 0.5 else "write"
            counter[kind] += 1
            aid = f"{'r' if kind == 'read' else 'w'}{tid}{seg[0]}{counter[kind]}"
            st = {kind: rng.randrange(blocks), "id": aid}
            if kind == "write":
                avail = readable + done_reads
                if seg == "body":
                    st["data"] = (avail and rng.random() < 0.6) and rng.choice(avail) or random_constant(rng, pool).value
                else:
                    st["data"] = T.to_value(random_expr(rng, avail, classes, pool, 2))
            steps.append(st)
            open_.append((aid, kind))
            pending -= 1
        else:
            aid, kind = open_.pop(rng.randrange(len(open_)))
            steps.append({"done": aid})
            if kind == "read":
                done_reads.append(aid)
    return steps, done_reads


def _events(rng, steps, k_count, relations, count):
    if not k_count or not count:
        return steps
    pairs = [(k, r) for k in range(k_count) for r in relations]
    chosen = rng.sample(pairs, min(count, len(pairs)))
    slots = sorted(rng.randint(0, len(steps)) for _ in chosen)
    by_k: dict[int, list[str]] = {}
    for k, r in chosen:
        by_k.setdefault(k, []).append(r)
    for rels in by_k.values():
        rels.sort(key=REL_RANK.__getitem__)
    ks = [k for k, _ in chosen]
    rng.shuffle(ks)
    events = [(slot, {by_k[k].pop(0): k}) for slot, k in zip(slots, ks)]
    out, ei = [], 0
    for i in range(len(steps) + 1):
        while ei < len(events) and events[ei][0] == i:
            out.append(events[ei][1])
            ei += 1
        if i < len(steps):
            out.append(steps[i])
    return out


def generate_loop(seed: int, threads: int = 2, blocks: int = 2, prefix: int = 1, body: int = 2, suffix: int = 1,
                  max_in_flight: int = 2, sync: bool = False, value_pool: int = 3,
                  classes: dict | None = None, attempts: int = 200) -> LoopSetup:
    rng = random.Random(seed)
    classes = classes or {"const": 0.4, "copy": 0.3, "combine": 0.3}
    rels = ["before", "after", "at"]
    for _ in range(attempts):
        counter = {"read": 0, "write": 0}
        tdocs = []
        for t in range(threads):
            pre, pre_reads = _segment(rng, t, "prefix", rng.randint(0, prefix), blocks, max_in_flight, value_pool,
                                      counter, [], classes)
            bod, _ = _segment(rng, t, "body", rng.randint(1, body), blocks, max_in_flight, value_pool,
                              counter, pre_reads, classes)
            suf, _ = _segment(rng, t, "suffix", rng.randint(0, suffix), blocks, max_in_flight, value_pool,
                              counter, pre_reads, classes)
            if sync:
                bod = _events(rng, bod, 1, rels, rng.randint(1, 2))
                pre = _events(rng, pre, 1, ["before", "at"], rng.randint(0, 1))
                suf = _events(rng, suf, 1, ["after", "at"], rng.randint(0, 1))
            tdocs.append({"id": f"t{t}", "prefix": pre, "body": bod, "suffix": suf})
        init = [random_constant(rng, value_pool).value if rng.random() < 0.7 else "*" for _ in range(blocks)]
        doc = {"format": "loop-setup", "version": 1, "id": f"loop-{seed}", "blocks": blocks,
               "sync_points": 1 if sync else 0, "loop_sync_points": 1 if sync else 0, "init": init, "threads": tdocs}
        try:
            return LoopSetup.from_doc(doc)
        except (MalformedSetup, ValueError, KeyError):
            continue
    raise RuntimeError(f"no valid loop setup for seed {seed}")
