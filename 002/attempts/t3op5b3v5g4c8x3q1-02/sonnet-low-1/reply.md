C4 can return 1, 2 or 4.

**Fixing the order on y.** The writes to y are A1 (value 1) and C3 (value 4).
- A4 returns 4, so C3 is the last write to y before A4. A1 precedes A4 in program order, so A1 takes effect before C3.
- B1 returns 1, so B1 comes after A1 and before C3.
- This gives the order A1 < B1 < C3 < A4.

**What C4 can see.** C4 follows C1, C2 and C3 in program order, so C1 (value 2) has taken effect and C4 cannot return 0. The writes to z are C1 (2), A2 (1) and B3 (the value B2 read, either 1 or 4). Nothing constrains where A2, B2 and B3 fall relative to C4, apart from A2 taking effect before A4.

- **C4 = 2:** A2 takes effect before C1, and B3 either comes after C4 or writes 1 before C1. C1 is then the last write to z before C4.
- **C4 = 1:** A2 takes effect after C1 and before C4. This is allowed because A4 only needs to come after C3, so A2 can sit between C3 and A4.
- **C4 = 4:** B2 reads y after C3 and so returns 4. B3 then writes 4 to z after C1 and before C4.
- **C4 = 5 is impossible**, because 5 is only ever written to x, never to z.

BEGIN
1
2
4
END