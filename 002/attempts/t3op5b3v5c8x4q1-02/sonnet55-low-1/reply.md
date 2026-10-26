Q1 can only be 0.

**C3 must return 1.** C3 comes after C1 (writes 5) and C2 (writes 1) in thread C. The only other write to y is B3, which writes 1. So the last write to y before C3 is always a 1, and C5 therefore writes 1 to z.

**The last z-write before A5 must be A3 with value 0.**
- A5 reads z and returns 0, and A3 has already written to z by then, so some write to z took effect before A5.
- The last of those writes must have written 0.
- B1 writes 4 and C5 writes 1, so neither can be that last write.
- So A3 must be the last write, and it writes the value A2 read. That value must be 0.

**A2 = 0 is achievable.** Order the steps like this:
1. A1, A2 (reads y = 0) and A3 (writes 0 to z) all happen first, before any write to y.
2. C1 and C2 then write y = 1, so A4 reads 1.
3. A5 reads z = 0 before B1 and C5 write to z.
4. All of thread B and C5 run after A5.

This satisfies every known result.

BEGIN
0
END