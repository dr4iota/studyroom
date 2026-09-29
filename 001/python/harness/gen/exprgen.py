"""Helpers for generating random expressions and other weighted choices.

The three content classes of premise.md §2.5:

``const``    class 1, a constant ``c``                         ``7``
``copy``     class 2, a constant plus one earlier read ``x``   ``r1~7``
``combine``  class 3, a tree over several reads and constants  ``r1~(r3~2)``

``copy`` and ``combine`` need at least one available read; without one they fall back
to ``const``. All functions take an explicit ``random.Random`` so output is seeded.
"""

from __future__ import annotations

import random
from typing import Mapping, Sequence, TypeVar

from ..terms import Const, Expr, Node, Pair, Ref

K = TypeVar("K")


def weighted_choice(rng: random.Random, weights: Mapping[K, float]) -> K:
    keys = [k for k, w in weights.items() if w > 0]
    if not keys:
        raise ValueError(f"no positive weight in {dict(weights)}")
    return rng.choices(keys, [weights[k] for k in keys])[0]


def zipf_weights(n: int, s: float) -> list[float]:
    return [1.0 / (i + 1) ** s for i in range(n)]


def random_constant(rng: random.Random, pool: int) -> Const:
    """A constant from ``1..pool``; small pools give repeated values (a hardness dial)."""
    return Const(rng.randint(1, max(1, pool)))


def const_expr(rng: random.Random, pool: int) -> Expr:
    return random_constant(rng, pool)


def copy_expr(rng: random.Random, reads: Sequence[str], pool: int) -> Expr:
    """``x~c`` for a random read ``x`` and constant ``c`` (the constant tags the write)."""
    return Pair(Ref(rng.choice(list(reads))), random_constant(rng, pool))


def combine_expr(rng: random.Random, reads: Sequence[str], pool: int, max_depth: int) -> Expr:
    """A random tree of depth ``1..max_depth`` with read and constant leaves.

    At least one leaf is a read; when two or more reads are available, at least two
    different reads are used.
    """
    reads = list(reads)
    must = rng.sample(reads, min(2, len(reads)))

    def leaf() -> Node:
        if must:
            return Ref(must.pop())
        return Ref(rng.choice(reads)) if rng.random() < 0.5 else random_constant(rng, pool)

    def tree(d: int) -> Node:
        if d == 0:
            return leaf()
        left = tree(rng.randint(0, d - 1)) if rng.random() < 0.5 else leaf()
        right = tree(d - 1)
        return Pair(left, right) if rng.random() < 0.5 else Pair(right, left)

    t = tree(rng.randint(1, max(1, max_depth)))
    while must:  # the tree had fewer leaves than required reads
        t = Pair(t, Ref(must.pop()))
    return t


def random_expr(rng: random.Random, reads: Sequence[str], classes: Mapping[str, float],
                pool: int, max_depth: int) -> Expr:
    """Draw a content class by weight, then an expression of that class."""
    cls = weighted_choice(rng, classes)
    if cls == "const" or not reads:
        return const_expr(rng, pool)
    if cls == "copy":
        return copy_expr(rng, reads, pool)
    if cls == "combine":
        return combine_expr(rng, reads, pool, max_depth)
    raise ValueError(f"unknown content class {cls!r}")
