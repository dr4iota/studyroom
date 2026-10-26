**Analysis**

Ordering constraints: B1<B2<B3<B4 all take effect before Q; A5 occurs between Q and P; B5 takes effect sometime after B4 (its start can be before Q, its end is after P). A1–A4 are only constrained to precede A5, so they may interleave freely with B1–B4.

- **A1** sees the last write to y before it: 0 (before B1), 1 (between B1 and B2), or 3 (after B2, or after B4 which can only rewrite 3 in that case). So A1 ∈ {0,1,3}.
- **B3** happens after B2, so it sees 3 unless A2 (writing A1's value) or A4 (writing 2) lands between B2 and B3. So B3 ∈ {3, A1's value, 2}.
- **Final y** is the later of A4 (2) and B5 (1). B5 can always be last → 1. A4 can be after B5 → 2, except when B3 = 2, which forces A4 < B3 < B4 < B5, so final y = 1.

BEGIN
0 3 1
0 3 2
0 0 1
0 0 2
0 2 1
1 3 1
1 3 2
1 1 1
1 1 2
1 2 1
3 3 1
3 3 2
3 2 1
END