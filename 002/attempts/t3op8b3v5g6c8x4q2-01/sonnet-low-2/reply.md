Q1 can be 1 or 5, and Q2 is always 4.

**Which write to z comes last.** The final value z = 1 can come from B1 (writes 1), from A7 if A3 returned 1, or from C8 if C6 returned 1.

**Facts that hold in every execution.**
- B2 reads 4 before any of B's own writes to y happen. The only other write of 4 to y is A4, so A4 takes effect before B2.
- A1 comes before A4, so y is never 0 or 1 again after A4 except through a later write of 1. No such write exists, because B3 reads y only after A4.
- B3 reads 4. If it read 5, B4 and B5 would write 5, and no later write of 4 could let B7 read 4. So B4 and B5 both write 4.
- C3 reads 5 and C4 then reads 4, so a write of 4 lands between C3 and C4.

**Q2 (C6).**
- C6 comes after C4, which read 4.
- From then on, the only writes to y are 4s (from A4, B4 and B5), so C6 = 4.
- C8 therefore cannot write 1, and the final z = 1 must come from B1 or A7.

**Q1 (A3).**
- A3 sits between A1 and A4 in thread A, so it reads y before any write of 4 can have happened. It cannot return 0 or 4.
- If A3 returns 1: this works both with B1 last on z and with A7 last on z. For example, run A1, A3, C1, C3, A4, C4, and so on.
- If A3 returns 5:
  - Run C1 first, then A1, then A3 (reads 5), then C3, then A4, then C4.
  - Here all of A and C finish before B1, so B1 is the last write to z.
  - B6 can then read x = 4, which A2 wrote.

BEGIN
1 4
5 4
END