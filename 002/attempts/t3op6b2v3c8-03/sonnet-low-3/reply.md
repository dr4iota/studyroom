Counting which values can reach block x:

- **Writers of x.** C1 and C5 write 3. C3 writes whatever C2 read. B4 writes whatever B2 read from y, which can be 0, 2 or 3. B6 writes what B5 read.
- **The value 2 in x.** It can only enter x through B4, when B2 read y=2. That needs A1 to take effect before B2, and B3 comes after B2.
- **Q2 (B1).** B1 precedes B4, so no 2 can be in x yet. B1 is 0 (before C1) or 3 (after C1).
- **Q1 (A2).** A2 can be 0, 2 or 3. A2=2 needs B4 to have written 2 first.
- **Q3 (C4).**
  - **C4=3:** C3 writes 3 after B4, or C4 simply sees C1's or C3's 3. All 6 combinations of A2 (0, 2, 3) and B1 (0, 3) work.
  - **C4=2:** B4 writes 2, with C3 before B4 or writing 2 itself, and C4 reads before C5. All 6 combinations of A2 and B1 work. A2=0 happens before C1. A2=3 happens after C1 and before B4. A2=2 happens after B4.
  - **C4=0:** B2 must read y=0, so B2 comes before A1, and B4 writes 0 after C1 and C3. Then x never holds 2 (C3 and B6 only copy 0 or 3), so A2 is 0 or 3 and B1 is 0 or 3. This gives 4 combinations.

That makes 16 combinations in total.

BEGIN
0 0 0
0 3 0
3 0 0
3 3 0
0 0 2
0 3 2
2 0 2
2 3 2
3 0 2
3 3 2
0 0 3
0 3 3
2 0 3
2 3 3
3 0 3
3 3 3
END