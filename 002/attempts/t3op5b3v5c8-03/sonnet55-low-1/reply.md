The block z is only ever written by A5, which writes the value A3 read. Since z starts at 0, A3 reads 0, so A4 writes 0 to y and z stays 0.

The writes to y are therefore A1 (3), A4 (0), B2 (5) and C1 (2). The ordering constraints are A1 before A4, and B1 before B2 before B4.

**B1** happens before B2, so it cannot return 5. It can return 0 (initial value or A4), 2 (C1 first), or 3 (A1 first).

**Final y** is the last write. A1 cannot be last because A4 follows it, so the final value is 0 (A4), 2 (C1) or 5 (B2).

**Final y = 5.** B2 is the last write, so B4 reads 5. B1 can be 0, 2 or 3. This gives (0,5,5), (2,5,5), (3,5,5).

**Final y = 0.** A4 is the last write.
- B1 = 0: B4 can be 5, 0, 2 or 3.
- B1 = 2: B4 can be 5, 0 or 3. B4 = 2 is impossible, since B4 reading 2 needs C1 after B2, but B1 = 2 needs C1 before B2.
- B1 = 3: B4 can be 5, 0 or 2. B4 = 3 is impossible, since B4 reading 3 needs A1 after B2, but B1 = 3 needs A1 before B2.

**Final y = 2.** C1 is the last write, so B1 cannot be 2.
- B1 = 0: B4 can be 5, 0, 3 or 2.
- B1 = 3: B4 can be 5, 0 or 2. B4 = 3 is impossible for the same reason as above.

BEGIN
0 5 5
2 5 5
3 5 5
0 5 0
0 0 0
0 2 0
0 3 0
2 5 0
2 0 0
2 3 0
3 5 0
3 0 0
3 2 0
0 5 2
0 0 2
0 3 2
0 2 2
3 5 2
3 0 2
3 2 2
END