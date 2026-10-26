**Answer:** Q1 (A4) can be 0, 1 or 5. Q2 (B2) is always 0. Q3 (final y) can be 3 or 4. All six combinations are possible.

**Q2: B2 must return 0.**
- The only writes to x are A3 and B3.
- B3 writes the value B2 read, and B4 runs after B3 and is known to read 0.
- So the value of x seen by B4 is 0. It comes either from B3 itself or from a later A3 that writes 0.
- Suppose B2 returned something other than 0. That value could only have come from A3, so A3 took effect before B2.
- Then B3 writes that nonzero value to x. A3 has already happened and cannot run again, so no later write could reset x to 0 before B4.
- B4 would then not read 0, which contradicts the known result. So B2 returned 0, and B3 writes 0.
- C4 also reads 0, which is consistent: no execution is forced to show a nonzero x.

**Q1: A4 can return 0, 5 or 1.**
- The writes to z are B1 (5), C2 (5) and C3 (1).
- A4 may take effect before all of them, giving 0.
- It may take effect after B1 or C2 and before C3 (or after C3 when B1 is placed last), giving 5.
- It may take effect after C3 when C3 is the last write to z, giving 1.
- In each case A1 and A2 can be placed consistently before A4. A3 then writes A1's value, and that does not break the B4 or C4 results in suitable orderings.

**Q3: the final y can be 3 or 4.**
- The only writes to y are C1 (4) and A5 (3).
- C1 has no ordering constraints with thread A, so either write can be the last one.
- This holds for every value of A4. For example, when A4 reads 0, C1 can still come after A5 (y = 4) or before it (y = 3).

BEGIN
0 0 3
0 0 4
1 0 3
1 0 4
5 0 3
5 0 4
END