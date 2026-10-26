Reading each sync line as a constraint on which steps may fall before or after each instant:

- A1–A3 happen before R, and B7–B9 happen after R, so A1–A3 happen before B7.
- A4 and later steps happen after P and after S.
- B1–B4 happen before S, and B5–B6 happen before P, so B1–B6 happen before A4.
- B1–B8 happen before Q, and A7 and A8 happen after Q, so B1–B8 happen before A7.

**Q3 (A7).**
- B5 reads x after B3 wrote 4. The only other writes to x are by A4 and A6, and both come after P, which is after B5. So B5 returns 4.
- B8 therefore writes 4 to y. B8 is before Q, and A7 is after Q.
- The only other writes to y are B2 (writes 2, which comes before B8) and A8 (after A7).
- So A7 always returns 4.

**Q1 (A2).**
- A2 is before R, so it is before B7, and B9 (writing 3) comes after B7. A5 comes after A3, which is after A2.
- The writes to z that A2 can see are therefore B1 (4) and B6 (writes B5's value, which is 4), or the initial 0.
- So A2 is 0 or 4.

**Q2 (A3).**
- Before A4, the only write to x is B3 (4), and A3 is before R, so it can fall on either side of B3.
- So A3 is 0 or 4.

**Combinations of A2 and A3.** Nothing orders A1–A3 against B1–B3, so every pairing is possible:
- (0, 0): A2 and A3 both run before B1 and B3.
- (0, 4): A2 runs before B1, and A3 runs after B3.
- (4, 0): A2 runs after B1, and A3 runs before B3.
- (4, 4): A2 and A3 both run after B1 and B3.

BEGIN
0 0 4
0 4 4
4 0 4
4 4 4
END