Because B1–B7 must all happen before S, and A starts only after S, the values of z are fixed:

- B2 reads z before B7 or A1 can write it, so B2 returns 0. B3 and B8 therefore both write 0 to y.
- B7 writes 1 to z before S, and A1 then writes 6 to z. So A6 and A8 both read 6, and Q2 is always 6.

**Q1 (A3).** A3 comes after A2, which writes 6 to y. Every other B write to y except B8 happens before S, so it is overwritten. B8 (writes 0) may land after A2 and before A3. So A3 is 6 or 0.

**Q3 (B9).** B9 reads x, which holds 5 (B1) unless A5 has already written. A5 writes whatever A4 read.
- A4 is 6, or 0 if B8 landed before it. It cannot be 4, because A7 comes after A4.
- If A3 is 0, B8 came before A3, so A4 is also 0. B9 is then 5 (read before A5) or 0 (after A5).
- If A3 is 6, A4 can be 6 or 0, so B9 can be 5, 6 or 0.
  - B9 = 6 needs B8 after A4 and A5 before B9.
  - B9 = 0 needs B8 between A3 and A4, with A5 before B9.

BEGIN
6 6 5
6 6 6
6 6 0
0 6 5
0 6 0
END