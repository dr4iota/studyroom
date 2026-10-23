Each outcome below is reached by an order of operations that the rules allow.

**What can change x.** There are three writes to x:
- B1 writes 1.
- B2 writes 3, after B1.
- A4 writes whatever A1 read; call that value a. A4 also comes after A3.

**When B3 and B4 read.** B3 and B4 both run after B2. A4 is the only write to x that can come after B2. So B3 and B4 each return either 3 (A4 has not happened yet) or a (A4 has happened).

**Case a = 0 (A1 happens before B1).** A3 can happen before B1, between B1 and B2, or after B2. So A3 can return 0, 1 or 3. A4 writes 0 at some point after A3:
- If A4 happens before B2, then B3 and B4 both return 3.
- If A4 happens after B2 and before B3, they both return 0.
- If A4 happens between B3 and B4, B3 returns 3 and B4 returns 0.
- If A4 happens after B4, they both return 3.

For each A3 value, at least one of these A4 positions is possible:
- A3 = 0 gives (0,3,3), (0,0,0), (0,3,0).
- A3 = 1 gives (1,3,3), (1,0,0), (1,3,0).
- A3 = 3 gives (3,3,3), (3,0,0), (3,3,0).

**Case a = 1 (A1 happens between B1 and B2).** A3 can happen before or after B2, so it returns 1 or 3. A4 writes 1:
- A3 = 1 gives (1,3,3), (1,1,1), (1,3,1).
- A3 = 3 gives (3,3,3), (3,1,1), (3,3,1).

**Case a = 3 (A1 happens after B2).** A3 and A4 then also come after B2. The only value x ever holds after that point is 3, so the only outcome is (3,3,3).

**Impossible pattern.** B3 can never return a and then B4 return 3. Once A4 has written a, nothing writes to x again.

BEGIN
0 3 3
0 0 0
0 3 0
1 3 3
1 0 0
1 3 0
1 1 1
1 3 1
3 3 3
3 0 0
3 3 0
3 1 1
3 3 1
END