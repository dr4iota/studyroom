Both B7 and A1 write z, and B7 ends before sync point S while A1 starts after S. So B1–B7 all finish before A1 and A2 start. B2 therefore reads z = 0, so B3 and B8 both write 0 to y.

**Q2 (A8):** z is written by B7 (value 1) and then by A1 (value 6), and A1 is the last write to z. A8 comes after A1 in thread A, so A8 always returns 6.

**Q1 (A3):** A3 comes after A2, which writes 6 to y. B3, B4 and B5 all finish before A2, so the only write that can land between A2 and A3 is B8, which writes 0. A3 returns 0 if B8 lands between A2 and A3. Otherwise A3 returns 6.

**Q3 (B9):** B9 reads x, which holds 5 from B1 until A5 writes. A5 writes whatever A4 read. A4 reads y after A2, so it returns 6, or 0 if B8 landed before it. B9 runs after B8, so it can return 5 if it comes before A5, or A5's value if it comes after. I checked each position of B8:

- **B8 before A2:** A3 = 6 and A4 = 6, so A5 writes 6. B9 can be 5 or 6.
- **B8 between A2 and A3:** A3 = 0 and A4 = 0, so A5 writes 0. B9 can be 5 or 0.
- **B8 between A3 and A4:** A3 = 6 and A4 = 0, so A5 writes 0. B9 can be 5 or 0.
- **B8 after A4:** A3 = 6 and A4 = 6, so A5 writes 6. B9 can be 5 or 6.

Collecting these gives A3 = 6 with B9 in {5, 6, 0}, and A3 = 0 with B9 in {5, 0}.

BEGIN
6 6 5
6 6 6
6 6 0
0 6 5
0 6 0
END