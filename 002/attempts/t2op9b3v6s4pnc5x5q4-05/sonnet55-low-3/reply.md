Every outcome below follows from tracing which writes can come before each read.

**A2 and the values A writes to x.** A2 ends before P, and every write to z by B (B3, B4, B7) comes after P, so A2 reads 0. That makes A3 and A7 both write 0 to x.

**Q4 equals Q2.** A5 (y=3) comes before S, and B5 comes after S, so B5 is the last write to y. B9 comes after B5, so B9 returns B2's value.

**Q2 (B2).** B2 reads x after P. It can return 3 (A1 is the last write so far), 5 (B1 is the last write), or 0 (A3 or A7 is the last write).

**Cases by B2's value** (columns are A8, B2, B8, B9):

- **B2 = 3.** B1 must come before A1, and B2 must come before A3. Then A3 and A7 write 0 and nothing writes 5 later, so A8 = 0 and B8 = 0. Outcome: 0 3 0 3.
- **B2 = 0.** B1 must be overwritten by a 0 write before B2 reads. Nothing writes a nonzero value to x afterwards, so A8 = 0 and B8 = 0. Outcome: 0 0 0 0.
- **B2 = 5.**
  - B2 before A3: A3 runs before Q and B8 runs after Q, so A8 = 0 and B8 = 0. Outcome: 0 5 0 5.
  - B1 after A3 and B2 before A7: A8 = 0. B8 comes after S but can come before or after A7, so B8 is 5 or 0. Outcomes: 0 5 5 5 and 0 5 0 5.
  - B1 and B2 after A7: B1 can fall before A8 (A8 = 5) or after it (A8 = 0). B8 comes after B2, so B8 = 5. Outcomes: 5 5 5 5 and 0 5 5 5.

BEGIN
0 3 0 3
0 0 0 0
0 5 0 5
0 5 5 5
5 5 5 5
END