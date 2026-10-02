# Sources

One algorithm is registered: `opus55_1-s-decomp` (in `counter.py`). It has several
parts. Each part's origin is given below. I used no web access and ran no code.

## Building the poset
This is my own construction, written from spec §2, §3 and §8. Each thread is one chain. An
`at` step is merged into its sync node, and that node goes on the chain of the first thread
that has an `at` on it. The partition is still a partition into chains. A sync node with
no `at` event is "free" and sits on no chain. Sync points that no event mentions are
isolated nodes and are only counted, never built.

## Independent parts and the multinomial
This is from memory and is standard: the linear extensions of a disjoint union are
interleavings, so `e(P ⊔ Q) = C(|P|+|Q|, |P|)·e(P)·e(Q)`. Threads that share no sync point
are independent groups. Within any piece I also take connected components.

## Ordinal-sum splitting
- **From memory (standard):** `e(P ⊕ Q) = e(P)·e(Q)`. Every ordinal split is a prefix of
  every linear extension.
- **Own derivation:** the detection method. Fix one topological order. A split after
  position `k` is valid unless some `a` before it is incomparable to some `b` after it. For
  each `a` I compute `far(a)`, the last position of an element that is not `≥ a`. A
  coverage sweep then gives every valid split.
- **Also my own derivation:** how `far(a)` is computed. On each chain, `up(a)` is a suffix
  of that chain, found with a "first position on chain c above a" vector. Free nodes are
  emitted right after the node that makes them ready, so only one small group of them needs
  checking.

## Down-set dynamic program
- **Adapted from memory:** the classic DP that counts linear extensions over order ideals.
  Each ideal is given by a position vector on a chain partition. This is the usual method
  for posets of bounded width; I do not have a specific paper in mind.
- **What I changed** (my own derivations) concerns the free sync nodes:
  - **No predecessors in the piece:** these are inserted lazily, just before their first
    successor. A node inserted into a prefix of `k` elements has `k+1` possible gaps.
  - **No successors in the piece:** these are kept as a counter of released nodes that
    have not yet been placed. They are interchangeable, so placing one multiplies by the
    counter.
  - **Both predecessors and successors:** the state stores the set of such nodes that are
    placed while their successors are not. The candidate set depends only on the position
    vector and is cached for each vector.
  - **Direction:** the DP runs on the reversed poset when that makes more nodes lazy.

## Memoisation and extrapolation in n
This is my own derivation.
- **Memo key:** each piece gets a canonical key from (step label, iteration relative to the
  piece's first iteration) and its edges. Equal keys mean isomorphic pieces, so translated
  copies are counted once.
- **Extrapolation:** for large `n`, I decompose the unrollings `P_m` for four consecutive
  values `m = m0 … m0+3`, with `m0 = 3·(threads in group) + 6`. Pieces whose keys appear in
  all four with affine multiplicities are raised to their extrapolated power. Growing pieces
  are matched across `m` by their set of labels and handled recursively. Their sizes must be
  affine, and they feed a multinomial or a product. If anything fails these checks, the
  code builds `P_n` and decomposes it directly. The direct path is exact for every `n`.

## Uncertainties
- **The extrapolation rests on an argument I have not proved fully.** Paths between body
  nodes never go back to an earlier iteration, and body edges are the same in every
  iteration. So comparabilities depend only on the difference in iteration, apart from
  boundary effects reaching about one iteration per thread from each end. On that basis I
  expect the decomposition to be eventually periodic, with a short head and tail, and
  `m0 = 3T+6` with four checked values is meant to be a safe margin.
- **Some cases stay slow.** The DP is exponential when many free sync nodes are open at the
  same time, for example a per-iteration sync point with only `before` in one thread and
  `after` in another, while those threads drift apart. Pieces that grow with `n` and cannot
  be decomposed are counted directly on `P_n`, which is polynomial in `n` but slow for
  large `n`.
