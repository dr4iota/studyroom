"""``fable51-s-cut``: cut-node decomposition; the product of the segments' Gray listings.

Idea
----
A node comparable with every other node (a *cut node*: a full ``at`` barrier across all
threads, or any step that every other step is ordered against) sits at the same position
in every linearization. The cut nodes split the poset into intervals, and ``Lin(P)`` is
the concatenation product ``Lin(S_1) x {c_1} x Lin(S_2) x ...`` (``common.cut_segments``).
Each interval is enumerated by the Pruesse–Ruskey listing (``fable51-s-pr``) on its induced
sub-poset, and the product is walked as an odometer, last segment fastest. Segments with
at most ``cache`` linearizations are listed once and replayed from memory, so that a tiny
last segment does not cost a generator restart per output.

Cost
----
Per output: ``O(1)`` amortized moves inside the fastest segment plus ``O(n)`` to
concatenate the tuple, plus the amortized restart cost of the inner generators
(``O(n_i^2)`` bits of closure per restart, once per outer step). Memory ``O(n)`` plus the
cached small listings (``cache * n`` ints at most per segment). Deterministic, lazy.
Adjacency: inside a segment consecutive outputs differ by one or two adjacent
transpositions (PR); at an odometer carry the inner segments jump back to their first
listing, so no global Gray property is claimed. Without cut nodes this is exactly
``fable51-s-pr``.
"""

from __future__ import annotations

from typing import Callable, Iterator

from harness.lin.api import LinEnumerator
from harness.model import Setup
from harness.poset import Linearization, TracePoset
from harness.registry import register

from . import pr
from .common import SYNC, SubPoset, cut_segments


def linear_extensions(P: TracePoset, cache: int = 1024) -> Iterator[Linearization]:
    n = len(P)
    if n == 0:
        yield ()
        return
    segs = cut_segments(P)
    subs = [SubPoset(P, s) for s in segs]
    m = len(segs)
    cached: list[list[Linearization] | None] = [None] * m

    def seg_iter(i: int) -> Iterator[Linearization]:
        if cached[i] is not None:
            return iter(cached[i])
        if len(segs[i]) == 1:
            cached[i] = [(segs[i][0],)]
            return iter(cached[i])
        nodes = subs[i].nodes

        def run() -> Iterator[Linearization]:
            buf: list[Linearization] | None = []
            for loc in pr.linear_extensions(subs[i]):
                o = tuple(nodes[x] for x in loc)
                if buf is not None:
                    if len(buf) < cache:
                        buf.append(o)
                    else:
                        buf = None
                yield o
            if buf is not None:
                cached[i] = buf

        return run()

    iters: list[Iterator[Linearization] | None] = [None] * m
    parts: list[Linearization] = [()] * m
    i = 0
    iters[0] = seg_iter(0)
    while i >= 0:
        nxt = next(iters[i], None)  # type: ignore[arg-type]
        if nxt is None:
            i -= 1
            continue
        parts[i] = nxt
        if i == m - 1:
            out: list[int] = []
            for p in parts:
                out.extend(p)
            yield tuple(out)
        else:
            i += 1
            iters[i] = seg_iter(i)


@register
class FableSyncCut(LinEnumerator):
    name = "fable51-s-cut"
    description = "cut-node segments (barriers) x Pruesse-Ruskey per segment, odometer product"
    capabilities = SYNC
    options = {"cache": "replay segments with at most this many linearizations from memory (default 1024)"}

    def enumerate(self, setup: Setup) -> Iterator[Linearization]:
        return linear_extensions(setup.poset, int(self.opts.get("cache", 1024)))
