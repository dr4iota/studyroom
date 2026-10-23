Every operation takes effect at a single instant, and there are no sync points. So the outcomes are exactly the interleavings that respect each thread's program order and the known results.

**Constraints**
- Thread A runs A1 < A2 < A3 < A4 < A5, and thread B runs B1 < B2 < B3 < B4 < B5.
- B5 returns 4, so A3 comes before B5. A2 returning 0 is automatic, because A2 comes before A3.
- B1 returns 0, so B1 comes before A5 (and before B2 anyway).
- The writes to x are B2 (2), B3 (1), B4 (2) and A5 (3). The sequence of values x passes through before A5 is 0, 2, 1, 2.

**Reads of x**
- A1 and A4 both come before A5, so neither can return 3.
- A1 can return 0, 2 or 1. It can return 2 either after B2 or after B4.
- A4 comes after A1, so it reads a value at or after A1's position in the sequence 0, 2, 1, 2.

**Final value of x**
- It is 3 if B4 comes before A5, and 2 if A5 comes before B4.
- Both orders are consistent with A3 before B5.

**Final = 3** (all B writes come before A5, so A4 can see any point in 0, 2, 1, 2):
- A1=0: A4 can be 0, 2 or 1.
- A1=2: A4 can be 2 or 1.
- A1=1: A4 can be 1 or 2. The 2 is the value B4 writes.

**Final = 2** (A5 comes before B4, so A4 sees only 0, 2, 1):
- A1=0: A4 can be 0, 2 or 1.
- A1=2: A4 can be 2 or 1.
- A1=1: A4 can be only 1.

These are all already in the final = 3 set. Every combination, with the final value, is listed below.

BEGIN
0 0 3
0 2 3
0 1 3
2 2 3
2 1 3
1 1 3
1 2 3
0 0 2
0 2 2
0 1 2
2 2 2
2 1 2
1 1 2
END