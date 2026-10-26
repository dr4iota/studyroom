Here, "state index" k means that the first k of B's writes have taken effect. The shared block then moves through the states 0, 3, 2, 1, 2 in that order, indexed 0 to 4. A4 writes 2 only after A1–A3 have finished.

**A2 and A3.** Both reads happen before A4, so they see only B's writes. They read at non-decreasing state indices i ≤ j. This gives these (A2, A3) pairs:
(0,0), (0,3), (0,2), (0,1), (3,3), (3,2), (3,1), (2,2), (2,1), (1,1), (1,2).

**A5.** A4 takes effect while the state index is k, with k ≥ j. A5 then reads either:
- 2, if no further B write takes effect before it, or
- the value of a later B write at some index m with k < m ≤ 4. Those values are 3 at index 1, 1 at index 3, and 2 at indices 2 and 4.

So A5 can always be 2. It can be 1 only if k ≤ 2, because the write of 1 is at index 3. It can be 3 only if k = 0.

Using the smallest j that gives each A3 value, the possible A5 values per pair are:
- (0,0): j=0, so 1, 2 and 3 are all possible.
- (0,3), (0,2), (3,3), (3,2), (2,2): 1 or 2.
- (0,1), (3,1), (2,1), (1,1), (1,2): only 2, because j ≥ 3.

BEGIN
0 0 1
0 0 2
0 0 3
0 3 1
0 3 2
0 2 1
0 2 2
0 1 2
3 3 1
3 3 2
3 2 1
3 2 2
3 1 2
2 2 1
2 2 2
2 1 2
1 1 2
1 2 2
END