Each operation takes effect at one instant, and there are no sync points. So every interleaving that keeps each thread's order is allowed, as long as B3 returns 3. I write a for the value A1 returns, b for B4's value, c for A4's value, and F for the final y.

**Constraint from B3 = 3.** The last write to x before B3 must be B2 or A5. This rules out exactly one case: A2 falls between B2 and B3 while A5 comes after B3.

**Possible values of a (A1).** x holds 0 before B1, 1 between B1 and B2, and 3 after B2. A1 comes before A2 and A5, so a is 0, 1 or 3.

**Possible values of b (B4).** The y writes are A3 (writes a), B5 (writes 2) and B6 (writes b). B4 comes before B5 and B6, so it sees either the initial 0 or A3's value. That gives b = 0 or b = a.

**Final y.**
- If A3 is the last y write, F = a.
- If B6 is the last y write, F = b.

**A4 (c).** A4 returns whichever y write took effect last before it: A3 (a), B5 (2) or B6 (b).

**Case a = 0.** A1 comes before B1, so b = 0 and F = 0. A4 sees 0 from A3 or B6, or 2 from B5. The c = 2 case is realised by A1, A2, B1, B2, B3, B4, A3, B5, A4, A5, B6. Outcomes: (0,0,0) and (0,2,0).

**Case a = 1.** A1 falls between B1 and B2.
- A3 after B6: A4 must see A3, so c = 1 and F = 1. Example: B1, A1, B2, B3, B4, B5, B6, A2, A3, A4, A5. Outcome (1,1,1).
- B6 last with b = 1 (B4 after A3): A4 sees A3 (c = 1) or B5 (c = 2), and F = 1. Example: B1, A1, B2, B3, A2, A3, B4, B5, A4, B6, A5. Outcomes (1,1,1) and (1,2,1).
- B6 last with b = 0 (B4 before A3): F = 0. Depending on where A4 falls, c = 1 (after A3), c = 2 (after B5) or c = 0 (after B6). Outcomes (1,0,0), (1,1,0) and (1,2,0).

**Case a = 3.** A1 falls after B2 and before A2. The same reasoning as for a = 1 applies with 3 in place of 1. One example is B1–B6 first, then A1–A5, giving (3,3,3). Outcomes: (3,3,3), (3,2,3), (3,0,0), (3,3,0) and (3,2,0).

BEGIN
0 0 0
0 2 0
1 1 1
1 2 1
1 0 0
1 1 0
1 2 0
3 3 3
3 2 3
3 0 0
3 3 0
3 2 0
END