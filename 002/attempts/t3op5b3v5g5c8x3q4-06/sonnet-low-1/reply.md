Every thread's operations take effect in program order, and with no sync points the threads can interleave freely.

**Constraint from A5.** A3 writes 2 to x, yet A5 later reads 0. So some write of 0 to x must land after A3 and before A5. Only B4 (writing B2's value) or C5 (writing C3's value) can do this.

**Possible values of B2 and C3.** The only values that can ever be in x are 0 and 2, so B2 and C3 are each 0 or 2.
- B2=2 and C3=2 is impossible. Nobody could write 0 into the window, because the only writes of x would be of 2.
- B2=2, C3=0 is possible with the order C3, A3, B2 (reads 2), C5 (writes 0), A5, and B4 (writes 2) after A5.
- B2=0, C3=2 is possible with the order B2, A3, C3 (reads 2), B4 (writes 0), A5.
- B2=0, C3=0 is possible.

**Final z.** The last write to z comes from B1 (5), C2 (1) or A4 (1). C1 (4) always precedes C2, so 4 is impossible.
- Final z=1 is achievable in all three cases.
- Final z=5 needs B1 to come after both A4 and C2.
  - In case (2,0), B2 comes after A3 and B1 comes before B2. The order C1, C2, C3, A1, A2, A3, A4, B1, B2, C5, A5 works.
  - In case (0,0), the order A1, C1, C2, C3 (reads 0), A2, A3, A4, C5 (writes 0), A5, B1, B2 works.
  - In case (0,2), B2 reads 0 so it precedes A3. B1 precedes B2, so B1 precedes A4 (which follows A3). Final z=5 is therefore impossible.

BEGIN
2 0 1
2 0 5
0 2 1
0 0 1
0 0 5
END