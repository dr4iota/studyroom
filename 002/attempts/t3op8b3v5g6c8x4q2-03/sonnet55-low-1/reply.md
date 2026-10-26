Both final z values are possible, but y can only end as 3.

**Where x = 2 comes from.** C2 reads x = 2. The writes to x are A1 (1), A2 (3), B2 (5), B6 (3), A8 (A7's value) and C5 (C2's value, which happens after C2). So A8 must have written 2, which means A7 read 2. A8 therefore comes after A7, A6 and A5, and before C2.

**Where x = 3 comes from.** C7 reads x = 3, after C5 has written 2. A2 comes before A8, which comes before C2, so A2 cannot be the write C7 sees. That write must be B6 (value 3), and B6 must come after C5 and before C7.

**Final y.** B7 comes after B6 in thread B, so B7 comes after C5, C2, A8 and A5. B7 writes 3 to y, so y ends as 3. B1 also writes 3 but happens earlier, so it cannot change this.

**Final z.**
- B4 reads 3, which must come from C1, so B3 comes before C1 and C1 comes before B4.
- B8 (writes 3) comes after B6, and C8 (writes 2) comes after C7. B6 and C7 are ordered with each other, and B8 and C8 have no ordering between them.
- C6 must read 3, which needs B5 or B8 to write 3 after C4. That is achievable in either order of B8 and C8.
- A3 can read 3 early, after C1 and before C3.

So B8 can be last (z = 3) or C8 can be last (z = 2).

BEGIN
3 2
3 3
END