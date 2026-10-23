**Constraints from the sync points**
- Thread A finishes entirely before P.
- B3 ends and B4 starts after P. B3 can start before P, so B3 can take effect before Thread A's reads.
- B4 takes effect after P, so after all of Thread A.
- Thread C finishes before Q. B1, B2 and B3 also happen before Q.

**What A3 needs.** A3 returns 2, so the last write to x before A3 is C1, C3, or B3 when B3 writes 2 (that is, when B2 returned 2).

**Case B2 = 1**

Here B2 reads y after B1 and before any C write to y. B3 then writes 1 to x.

- **A1 = 1:** B3 must take effect before A1. So B1, B2 and B3 all come before A1, and a C write of 2 to x comes between A1 and A3.
  - B1 is already done when A2 runs, so A2 reads 1 (B1) or 2 (C2 placed after B2).
  - A2 = 0 is impossible.
- **A1 = 0:** A1 runs before any write to x. A2 can be:
  - 0: A2 runs before B1 and C2.
  - 1: A2 runs after B1 and before C2.
  - 2: C2 runs after B2 and before A2.

  C1 then makes A3 read 2.
- **A1 = 2:** C1 runs before A1. A2 can be 0, 1 or 2 by the same placements.

**Case B2 = 2**

B2 reads y after C2 (or C4) and after B1, and B3 writes 2 to x.

- **A1 = 1** is impossible, because no write puts 1 into x.
- **A1 = 0:** A2 can be:
  - 0: A2 runs before any write to y.
  - 1: order C2, then B1, then A2, then C4, then B2.
  - 2: A2 runs after C2.
- **A1 = 2:** A2 can likewise be 0, 1 or 2.

BEGIN
0 0 1
0 1 1
0 2 1
1 1 1
1 2 1
2 0 1
2 1 1
2 2 1
0 0 2
0 1 2
0 2 2
2 0 2
2 1 2
2 2 2
END