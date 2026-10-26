**Key constraints**

- Program order within each thread.
- "before S" / "after S" (A1 before S, B5 after S) gives A1 < B5.
- P: B1 is before P and A3 onward is after P, so B1 < A3.
- Q: B2 is before Q and A9 is after Q, so B2 < A9.
- R: A9 is before R and B8, B9 are after R, so A9 < B8.
- A2 has no sync constraint beyond program order.

**Derived values**

- **a4** (A4 reads z): A1 and B1 are both before A4, so a4 is 1 if B1 is later than A1, and 6 if A1 is later. Both orders are feasible.
- **a7** = a4, since A6 writes a4 to z just before A7.
- **y**: only A8 writes y, so final y = a4.
- **z**: B8 is always the last write to z, so final z = b2, and B9 reads b2 as well (Q1 = b2).
- **b2** (B2 reads y): it is a4 if A8 precedes B2, otherwise 0.
- **x**: final x is 4 if B7 comes after A2, otherwise 1 (B7 is always after B5 and B6).

**Feasible combinations** (Q1 = b2, Q2 = final x, Q3 = final y, Q4 = final z)

- a4=1, b2=1: forced A8 < B2, so A2 < B7 and x=4. Result: `1 4 1 1`.
- a4=1, b2=0: x=1 (B7 < A2) and x=4 (A2 < B7) are both feasible. Results: `0 1 1 0` and `0 4 1 0`.
- a4=6, b2=6: forced A8 < B2, so x=4. Result: `6 4 6 6`.
- a4=6, b2=0: x=1 and x=4 are both feasible. Results: `0 1 6 0` and `0 4 6 0`.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END