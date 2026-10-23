Possible values of y are 0, 2 and 3. Write y=2 comes only from B2. Writes of 0, 3 or 2 come only from C4, which copies whatever C3 read from x. Block x can hold 0, 3, or 2 (the last only when A3 copies a 2 from y).

**Q3 (C1):** C1 runs before C4, so it can never see C4's write. A value of 3 in y can only come from C4. So C1 is 0 or 2.

**Q1 (A1):** A1 can see any value in y's history, so it is 0, 2 or 3. It is 3 only if C4 has already written 3.

**Q2 (B3):** B3 runs after B2, so it sees either 2 or C4's value if C4 landed after B2. C4's value can be 0, 3 or 2. So B3 is 0, 2 or 3. It is 3 only if C4 wrote 3.

**Combinations:**
- A1 = 0 or 2: every B3 in {0, 2, 3} works with every C1 in {0, 2}. For example, B3 = 0 uses C3 reading x = 0 before B1, then C4 writing 0 after B2. That gives 12 combinations.
- A1 = 3: y must contain C4's 3, so B3 can only be 2 or 3. B3 = 0 is impossible because the history would then be 0, 2, 0 or 0, 0, 2 with no 3. With C1 in {0, 2}, that gives 4 combinations.

BEGIN
0 0 0
0 0 2
0 2 0
0 2 2
0 3 0
0 3 2
2 0 0
2 0 2
2 2 0
2 2 2
2 3 0
2 3 2
3 2 0
3 2 2
3 3 0
3 3 2
END