Every operation on y can interleave freely, subject only to each thread's own order. Only x and z are untouched by anything that matters, and B2 is consistent with x = 0.

**Q1, the value returned by A2.** A1 runs before A2, so A2 cannot return 0. A3 runs after A2, so it cannot return 4. A2 returns 3 if no B write lands between A1 and A2. It returns 1 if only B4 lands between them, and 2 if both B4 and B5 do.

**Q2, the value returned by B3.** B3 runs before B4 and B5, so it cannot return 1 or 2. It returns 0 if it runs before A1, 3 if it sees A1 or A4, and 4 if it sees A3.

**Q3, the final value of y.** The last write overall is either A4 (value 3) or B5 (value 2), and both orders are possible.

**Combinations:**
- **A2 = 1:** B4 falls between A1 and A2, so B3 runs before B4. B3 is 0 or 3 (B3 cannot be 4, because A3 comes after A2). B5 runs after A2, so the final value is 3 or 2. This gives (1,0,3), (1,0,2), (1,3,3) and (1,3,2).
- **A2 = 2:** B5 runs before A2, so A4 is the last write and the final value is 3. B3 is 0 or 3. This gives (2,0,3) and (2,3,3).
- **A2 = 3:** B3 can be 0, 3 or 4, and the final value can be 3 or 2 in each case. This gives (3,0,2), (3,0,3), (3,3,2), (3,3,3), (3,4,2) and (3,4,3).

BEGIN
1 0 2
1 0 3
1 3 2
1 3 3
2 0 3
2 3 3
3 0 2
3 0 3
3 3 2
3 3 3
3 4 2
3 4 3
END