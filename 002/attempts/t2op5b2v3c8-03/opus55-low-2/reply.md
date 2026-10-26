Outcomes enumerated below; there are no sync points, so any interleaving that respects each thread's order is allowed.

**What B1 can read.** B1 reads y, which only Thread A writes before B4.
- B1 before A1 gives v = 0.
- B1 between A1 and A2 gives v = 2.
- B1 after A2 gives v = 1, because A2, A3 and A5 all write 1.

B2 then writes v to x. Only A4 (writes 3) and B2 (writes v) ever write x.

**Q1 (B3).** B3 runs after B2, so x holds either v or 3.
- B3 = 3 if A4 takes effect between B2 and B3.
- Otherwise B3 = v. In that case A4 is either before B2 or after B3.

**Q2 (B5).**
- If B3 = 3, then A4 was already the last write to x, so B5 = 3.
- If B3 = v, then B5 = 3 when A4 falls between B3 and B5, and B5 = v otherwise.

**Q3 (final y).** The last write to y is either A5 (writes 1) or B4 (writes the value B3 read).
- Case B3 = v, B5 = v:
  - If A4 is after B5, then A5 is too, so final y = 1.
  - If A4 is before B2, A5 can land before or after B4. So final y is v or 1.
  - This works for every v. For example, v = 0 is possible with A1–A4 all between B1 and B2.
- Case B3 = v, B5 = 3: A4 is between B3 and B5. A5 can still land before or after B4, so final y is v or 1.
- Case B3 = 3: here B5 = 3. A5 can land before or after B4, so final y is 3 or 1.

**Combining the cases:**
- B3 = v, B5 = v: (0,0,0), (0,0,1), (2,2,2), (2,2,1), (1,1,1)
- B3 = v, B5 = 3: (0,3,0), (0,3,1), (2,3,2), (2,3,1), (1,3,1)
- B3 = 3: (3,3,3), (3,3,1)

BEGIN
0 0 0
0 0 1
2 2 2
2 2 1
1 1 1
0 3 0
0 3 1
2 3 2
2 3 1
1 3 1
3 3 3
3 3 1
END