All 12 combinations of A1 ≤ A2 (from 0, 1, 2) and B2 (from 0, 1) are possible.

**Timing constraints**
- **Thread C:** every step of C happens before P. So C1 (y=1), C2 (y=2) and C3 (x=1) all take effect before P.
- **B1:** B1 returned 0, so it took effect before C1. B1 also happens before R.
- **B4:** B4 starts before Q and ends after Q and after P.
- **A5:** A5 starts before Q and ends after Q. So A1 through A4 all finish before Q.
- **A2:** A2 ends after R. Its start and its moment of effect are unrestricted, so it can take effect early.
- **No order between P, Q and R** is given, and none can be derived that blocks any combination below.

**Possible values of y over time**
y starts at 0. C1 sets it to 1, then C2 sets it to 2, and B3 also writes 2. The value never goes back down, so y moves 0 → 1 → 2 and stays at 2.
- **A1:** it can take effect before C1, between C1 and C2, or after C2. So it can return 0, 1 or 2.
- **A2:** it comes after A1 in the same thread. So it returns a value at least as large as A1's: 0, 1 or 2 with A1 ≤ A2.
- **A3 returned 2:** this only requires A3 to take effect after C2. That fits all of the cases above.

**Possible values of x for B2**
x can only become 1, written by C3 or A5.
- **B2 = 0:** B2 takes effect before C3 and before A5. B2 comes after B1, which is before C1, so this works.
- **B2 = 1:** B2 takes effect after C3.

**Combinations**
No constraint links B2 to A1 or A2. So each of the 6 pairs (A1, A2) with A1 ≤ A2 combines with B2 = 0 or 1, giving 12 combinations.

BEGIN
0 0 0
0 0 1
0 1 0
0 1 1
0 2 0
0 2 1
1 1 0
1 1 1
1 2 0
1 2 1
2 2 0
2 2 1
END