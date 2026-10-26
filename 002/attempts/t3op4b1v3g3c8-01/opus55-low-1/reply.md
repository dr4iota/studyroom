**Approach.** The writes are A3 (writes A1's value), B1 = 2, B4 (writes B2's value), C1 = 2, C2 = 3, C3 = 2 and C4 = 1. Since B4 comes after B3, and B3 must read 1, the final value is set by either B4 or A3.

**Why C4 must come before B3.** B3 returns 1. The only writes that can give 1 are C4, or A3 when A1 read 1. A1 can only read 1 if C4 came before it. So in every valid execution, C4 takes effect before B3.

**B2 = 2 (B1, C1 or C3 is the last write before B2)**
- Final 2: B1, A1 = 2, A2 = 2, B2 = 2, C1–C4, B3 = 1, A3 writes 2, B4 writes 2.
- Final 0: A1 = 0 (before any write), then B1, A2 = 2, B2 = 2, C1–C4, B3 = 1, B4 writes 2, A3 writes 0.
- Final 3: B1, B2 = 2, C1, C2, A1 = 3, C3, A2 = 2, C4, B3 = 1, B4 writes 2, A3 writes 3.
- Final 1: B1, B2 = 2, C1–C4, B3 = 1, A1 = 1, B4 writes 2, A2 = 2, A3 writes 1.

**B2 = 3 (C2 is the last write before B2)**
- Order: B1, C1, C2, B2 = 3, C3, C4, B3 = 1, B4 writes 3.
- A3 placed last gives final 0, 2 or 3, depending on whether A1 read 0, 2 or 3.
- Final 1 is impossible. A1 = 1 needs C4 before A1, and then A2 needs a write of 2 after C4. The only writes after C4 are B4 (writes 3) and A3, so A2 cannot read 2.

**B2 = 1 (B2 comes after C4)**
- Here B4 writes 1, so final 1 is possible.
- Finals 0, 2 and 3 come from putting A3 last with A1 = 0, 2 or 3. For example, A1 = 0 first, then C1, A2 = 2, the rest of C, B1, B2 = 1, B3 = 1, B4, and finally A3 writes 0.

**B2 = 0**
- B1 writes 2 before B2, so B2 can only read 0 if A3 writes 0 in between. That requires A1 = 0.
- Order: A1 = 0, B1, A2 = 2, A3 writes 0, B2 = 0, C1–C4, B3 = 1, B4 writes 0.
- A3 must come before B2, so B4 is the last write and the final value is 0.

BEGIN
2 0
2 1
2 2
2 3
3 0
3 2
3 3
1 0
1 1
1 2
1 3
0 0
END