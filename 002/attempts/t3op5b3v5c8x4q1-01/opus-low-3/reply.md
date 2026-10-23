**C4 can only return 2.**

**What must hold.**
- **B4 returns 2.** B4 comes after B3 (write 4 to y). So some write of 2 to y takes effect between B3 and B4. That write is either C2 or A2, and A2 writes 2 only if A1 read 2.
- **C3 returns 2.** z is written only by A4 and A5, and both write what A3 read. So A3 read 2, and A4 takes effect before C3. That puts A2, which comes before A3, before C3 and therefore before C4.
- **C2 comes before C4** in thread C. So C4 cannot return 0.

**Can C4 return 4?** C4 would need B3 to be the last write to y before C4. Then every write of 2 to y would have to take effect before B3. That leaves no write of 2 between B3 and B4, so B4 could not return 2. This is impossible.

**Can C4 return the value A2 wrote, if A1 read 0 or 4?** A2 would have to be the last write to y before C4. C2 also comes before C4, so C2 would have to come before A2. Then A1, which comes before A2, could read 0 only if C2 came after A1. It could read 4 only if B3 were the last write before A1. In both cases A2 itself comes after C2 and before A3. A3 would then read A2's value of 0 or 4, not 2, which contradicts C3 returning 2. So A2 can only matter when it writes 2.

**An execution where C4 returns 2:**
1. B1 and B2 write 4 and 3 to x, and C1 writes 4 to x.
2. B3 writes 4 to y.
3. C2 writes 2 to y, and B4 reads 2.
4. A1 reads 2, and A2 writes 2 to y.
5. A3 reads 2, and A4 and A5 write 2 to z.
6. C3 reads z = 2, and C4 reads y = 2.

BEGIN
2
END