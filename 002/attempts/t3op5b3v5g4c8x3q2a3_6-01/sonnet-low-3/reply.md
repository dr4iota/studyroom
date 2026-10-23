Only A2 and A4 write values that A1 read, so I first fixed what A1 reads and then used C2 to constrain C4.

**Block y:** the only writes to y are A2's, and A2 writes whatever A1 read. By induction y always holds 0, so A1 returns 0. A2 writes 0, and A4 writes 0 to x. B3 returning 0 is consistent with this.

**Block x:** the only writes are B1 (writes 1) and A4 (writes 0). The final value of x is whichever of these takes effect last.

**Constraint from C2 returning 3:**
- The only writers of 3 are B2 and B4, and C1 must come before C2.
- The last write to z before C2 must therefore be a 3, so B2 or B4 takes effect after C1 and before C2.
- B1 precedes B2 and B4 in thread B, so B1 happens before C2.
- C4 comes after C2 in thread C, so B1 happens before C4.

**Cases for A4 relative to B1 and C4:**
- A4 before B1: C4 reads 1 and the final x is 1.
- A4 between B1 and C4: C4 reads 0 and the final x is 0.
- A4 after C4: C4 reads 1 and the final x is 0.

C4 reading 0 with a final x of 1 is impossible. It would need A4 to take effect before C4 and B1 to take effect after A4. But B1 must come before C4, so C4 would then read 1.

Each of the three cases can be scheduled. A5 comes after A4, and A5 writes 2 to z. It can be placed before C1 or after C2, so it never interferes with C2 reading 3.

BEGIN
1 1
1 0
0 0
END