The asked values are Q1 = B1's read, Q2 = B3's read, and Q3 = the final value of x. There are no sync points, so the outcomes are exactly the interleavings of A1–A5 with B1–B4 that keep each thread's order. Every such interleaving is possible, and I enumerated their results.

**Key observations**

- A2 always precedes A3, so A3 reads 1 unless B4 lands between A2 and A3, in which case it reads B4's value r2.
- B4 comes after B1, B2, and B3, so those three reads see only A's writes.
- B2 reads the state after A's writes up to its position, so r2 is that value. B4 then writes r2.
- The final value is 2 (from A5) unless B4 comes after A5, in which case it is r2.

**Outcomes by where B4 falls**

- **B4 after A5:** the final value is r2, and A3 reads 1. The reads of B1, B2, and B3 can take values 0, 3, 1, or 2 in the order allowed by the timeline. This gives 20 distinct outcomes.
- **B4 before A5:** the final value is 2. The outcomes are (Q1, Q2) pairs from {(0,0), (0,3), (0,1), (3,3), (3,1), (1,1)}, each with final 2, giving 6 outcomes.

That gives 26 distinct combinations in total.

BEGIN
0 0 0
0 0 2
0 1 0
0 1 1
0 1 2
0 1 3
0 2 0
0 2 1
0 2 2
0 2 3
0 3 0
0 3 2
0 3 3
1 1 1
1 1 2
1 2 1
1 2 2
2 2 2
3 1 1
3 1 2
3 1 3
3 2 1
3 2 2
3 2 3
3 3 2
3 3 3
END