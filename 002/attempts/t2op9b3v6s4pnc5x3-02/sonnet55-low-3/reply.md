Reading the sync lines gives these constraints:

- A1–A3 all end before R, and B7 starts after R. So A1–A3 finish before B7 starts.
- B1–B6 all end before P, and A4 starts after P, so B1–B6 finish before any of A4–A8.
- B1–B8 all end before Q, and A7 starts after Q, so B8 finishes before A7 starts.

**B5:** B5 happens before P, so it happens before A4, which is the first write A makes to x. The only other write to x is B3 (4), and B3 precedes B5 in thread B. So B5 reads 4, and B6 writes 4 to z.

**Q1 (A2):** Writes to z that can precede A2 are B1 (4) and B6 (4), since A5 and B9 come after A2 is forced to finish. So A2 returns 0 or 4.

**Q2 (A3):** A3 reads x before R, and the only write to x that can precede it is B3 (4), since A4 and A6 come after P. So A3 returns 0 or 4.

**Joint (A2, A3):** A3 comes after A2 in thread A, and B3 comes after B1 in thread B, so each pairing can happen:
- (0, 0): A2 and A3 both run before B1 and B3.
- (0, 4): A2 runs before B1, then A3 runs after B3.
- (4, 0): A2 runs after B1, then A3 runs before B3.
- (4, 4): A2 and A3 both run after B3.

**Q3 (A7):** A7 starts after B8, which wrote 4 to y (the value B5 read). B2 wrote 2 earlier, and B8 comes after it. A8 comes after A7. So A7 always returns 4.

BEGIN
0 0 4
0 4 4
4 0 4
4 4 4
END