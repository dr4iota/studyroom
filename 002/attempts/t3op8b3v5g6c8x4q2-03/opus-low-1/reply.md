**Answer:** final y is always 3; final z can be 2 or 3.

**1. Where x = 2 comes from (C2).**
- The only writes to x are A1 (1), A2 (3), B2 (5), B6 (B4's value, which is 3), C5 (C2's value) and A8 (A7's value).
- C5 comes after C2, so it cannot be the source. That leaves A8.
- So A7 read y = 2, and C2 takes effect after A8. That means C2 is after every operation of thread A.

**2. Final value of y.**
- The writes to y are A4 (3), A5 (2), B1 (3) and B7 (3).
- C7 reads x = 3. That needs B6 (writing 3) to take effect after C5. B6 also has to come after A8, or C2 could not read 2.
- B7 comes after B6, so B7 is after all of thread A. B1 comes before B7 in thread B.
- So B7 is the last write to y, and y = 3.

**3. Constraints on z.**
- B4 reads z = 3. After B3 writes 2, a 3 must be written before B4. Only C1 can do that, since B5 and B8 come after B4. So the order is B3, then C1, then B4.
- A3 reads z = 3, from C1 or from B5. B8 is too late, because it comes after B6, which is after thread A.
- C6 reads z = 3 after C4 writes 4. So B5 or B8 must write 3 to z between C4 and C6.
- C8 then writes 2 to z.

**4. Final value of z.**
- It depends only on whether B8 takes effect before or after C8.
- **z = 3:** C4, B5, C5, B6, C6, C7, C8, B8. Here B8 is the last write to z.
- **z = 2:** the same order, but with B8 just before C8. Here C8 is the last write to z.

Both orders satisfy every known read result.

BEGIN
3 2
3 3
END