Without sync points, the threads can interleave in any order that keeps each thread's own steps in sequence.

**Possible values of y seen by A3 and A4**
- y starts at 0. B3 then writes 4, and later B4 writes 2.
- So y only ever goes 0 → 4 → 2.
- A3 reads before A4, so A4 can never see an earlier value than A3 did.
- That allows six pairs (A3, A4): (0,0), (0,4), (0,2), (4,4), (4,2), (2,2).

**Possible values of x seen by B2**
- B2 returns 0 if it takes effect before A1, and 3 if it takes effect after A1.

**Whether these choices are independent**
- The only links between the threads are that A1 comes before A3 and that B2 comes before B3.
- If B2 returns 0, the order B2 < A1 < A3 still lets B3 and B4 fall before, between or after A3 and A4. So all six pairs work.
- If B2 returns 3, the order A1 < B2 < B3 still lets A2, A3 and A4 come before B3, between B3 and B4, or after B4. So all six pairs work again.
- That gives 6 × 2 = 12 combinations.

BEGIN
0 0 0
0 0 3
0 4 0
0 4 3
0 2 0
0 2 3
4 4 0
4 4 3
4 2 0
4 2 3
2 2 0
2 2 3
END