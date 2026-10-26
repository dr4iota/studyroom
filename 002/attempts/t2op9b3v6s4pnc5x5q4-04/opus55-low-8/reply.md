**Ordering constraints from the sync points**
- **P:** B1 happens before A3 through A9.
- **Q:** B1 and B2 happen before A9.
- **R:** A1 through A9 happen before B8 and B9.
- **S:** A1 happens before B5 through B9.

**Value of z read by A4**
- The writes to z that can come before A4 are A1 (writes 6) and B1 (writes 1). B1 must come before A3.
- A6 and A9 come after A4, and B8 comes after R, so they cannot affect A4.
- So A4 returns 6 if B1 comes before A1, and 1 if B1 comes after A1. Call this value v, where v is 6 or 1.

**Value of y (A7, A8)**
- A6 writes v to z. B1 cannot come after A6, and B8 comes after R, so nothing else writes z between A6 and A7.
- So A7 returns v, and A8 writes v to y.
- A8 is the only write to y, so the final y is v.

**Value read by B2**
- B2 reads y. It returns 0 if it happens before A8.
- It returns v if it happens after A8. This is allowed, because B2 only has to come before A9.

**B9 and the final z**
- B8 writes B2's value to z.
- All of A's writes to z come before R, so nothing writes z after B8.
- So B9 equals B2's value, and the final z also equals B2's value.

**Final value of x**
- B7 writes 4 to x.
- A2 writes 1 to x and has no constraint relative to B7, as long as A2 comes before A3 through A9.
- So the final x is 4 if A2 comes before B7, and 1 if A2 comes after B7.
- If A2 comes after B7, then the chain B2 → … → B7 → A2 → A8 puts B2 before A8. In that case B2 returns 0.

**Combinations (B9, final x, final y, final z)**
- With final x = 4:
  - B2 returns 0, with v = 6 or v = 1. This gives 0 4 6 0 and 0 4 1 0.
  - B2 returns v. This gives 6 4 6 6 and 1 4 1 1.
- With final x = 1, B2 must return 0. This gives 0 1 6 0 and 0 1 1 0.

BEGIN
0 4 6 0
0 4 1 0
6 4 6 6
1 4 1 1
0 1 6 0
0 1 1 0
END