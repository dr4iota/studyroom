With no sync points, every interleaving that keeps each thread's own order is allowed.

**Q2: what B3 can return.** B3 reads y, and the writes to y are A1 (4), A2 (1) and B2 (1). B3 must come after B2.
- B3 returns 1 if B2 or A2 is the last write to y before it.
- B3 returns 4 if the order is B2 < A1 < B3 < A2.
- So B3 is 1 or 4.

**Q1: what A3 can return.** A3 reads x, and the writes to x are B4 (the value B3 read), C2 (2) and C3 (1).
- A3 returns 0 if all three writes come after it.
- A3 returns 1 or 2 if C3 or C2 is the last write before it.
- A3 returns 4 if B3 read 4 and B4 is the last write to x before A3.
  - For B3 to read 4, the order B2 < A1 < B3 < A2 is needed. A2 < A3 then holds by thread order.
  - Also C2 < C3 < B4 < A3 is needed, so B4 is the last write to x.
- A3 returning 4 is only possible when B3 returned 4.

**Q3: the final value of z.** The writes to z are A4 (A3's value), B1 (4), C4 (C1's value) and C5 (4). C5 comes after C4, so C4 can never be the last write.
- The final z is 4 if B1 or C5 is the last write.
- The final z equals A3's value if A4 is the last write.
- Both choices can be scheduled for every combination of A3 and B3 above. When A3 is 4, both choices give 4.

BEGIN
0 1 4
0 1 0
1 1 4
1 1 1
2 1 4
2 1 2
0 4 4
0 4 0
1 4 4
1 4 1
2 4 4
2 4 2
4 4 4
END