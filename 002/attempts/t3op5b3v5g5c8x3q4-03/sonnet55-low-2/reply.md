Working from the known results:

**y.** The only writes to y are C1 (value 2) and B4 (the value B1 read). B5 returned 2 and the only write to z that can carry 2 is B3, so B1 read 2 and B3 wrote 2. B1 can read 2 only after C1, since nothing else writes 2 to y earlier. B4 then writes 2 as well, so y ends at 2 (Q3 = 2). B2 runs after B1 and C1, and y never holds anything but 0 or 2, so B2 returns 2 (Q1 = 2).

**z.** C2 returned 3, so A1 is the last write to z before C2. That means C2 comes before B3 and before A4. B5 returned 2, so B3 comes before B5, and A4 is not between B3 and B5. Two orders are possible:
- A4 before B3, which gives a final z of 2.
- A4 after B5, which gives a final z of 4.

**x.** C4 reads after C3, which writes 5. A3, which writes 2, can also land between C3 and C4. For example, the order C1, A1, A2, C2, C3, A3, C4 is consistent with every constraint, and so is any order where A3 comes after C4 or before C3. Both outcomes (2 and 5) work with either final z.

BEGIN
2 2 2 2
2 2 2 4
2 5 2 2
2 5 2 4
END