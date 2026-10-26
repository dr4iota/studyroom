Rule 6 gives no sync points here, so any interleaving of the three threads' operations is allowed.

**B3 (read of y):** B2 has already written 1 before B3 runs. A1 can write 4 after B2 and before B3, as long as A2 comes later. So B3 is 1 or 4.

**A3 (read of x):** x can be written by C2 (2), C3 (1), or B4 (the value of B3, so 1 or 4). If none of these has happened yet, A3 reads 0. So A3 is 0, 1, 2 or 4.
- A3 = 4 needs B4 to have written 4, so B3 = 4. That is feasible: B3 reads 4 before A2, A3 comes after A2, and C2 and C3 come before B4.
- A3 = 0, 1 or 2 can pair with either B3 = 1 or B3 = 4. With B3 = 4, A3 only needs to run after A2, which is after B3, and read x before B4 changes it.

**Final z:** The last writer of z is one of B1 (4), A4 (the value of A3), or C5 (4). C4 always runs before C5, so it cannot be last.
- z = 4 is always achievable by running C5 last.
- z = A3's value is achievable by running A4 after B1 and C5, since A3 can read early and A4 can run late.
- For A3 = 4 both options give 4.

BEGIN
0 1 0
0 1 4
0 4 0
0 4 4
1 1 1
1 1 4
1 4 1
1 4 4
2 1 2
2 1 4
2 4 2
2 4 4
4 4 4
END