Every combination is listed below. Let a be the value A1 returns and b the value B4 returns.

**Constraints**
- **A1:** A1 runs before A2 and A5, so it can only see 0 (before B1), 1 (after B1, before B2) or 3 (after B2). So a ∈ {0, 1, 3}.
- **B4:** B4 sees either the initial 0 or the value A3 wrote. So b ∈ {0, a}.
- **A4:** A4 returns the last write to y before it. That is a from A3, or 2 if B5 falls between A3 and A4, or b if B6 falls between A3 and A4.
- **Final y:** If A3 takes effect after B6, the final value is a. Otherwise it is b.
- **B3 must return 3:** Either A2 takes effect before B2, or B3 takes effect before A2. Each case below has an order that meets this.

**Case a = 0** (A1 before B1)
- b must be 0, so the final y is 0.
- A4 returns 0. It returns 2 if B5 falls between A3 and A4.
- Outcomes: 0 0 0 and 0 2 0.

**Case a = 1** (A1 after B1, before B2)
- When b = 0, B4 is before A3.
  - Outcome 1 1 1: all of B runs, then A3 and A4. Order: B1, A1, A2, B2, B3, B4, B5, B6, A3, A4, A5.
  - Outcome 1 1 0: Order: B1, A1, A2, B2, B3, B4, A3, A4, B5, B6.
  - Outcome 1 2 0: B5 falls between A3 and A4, and B6 is after A4.
  - Outcome 1 0 0: B5 and B6 both fall between A3 and A4.
- When b = 1, B4 is after A3. Then B6 is after A3, so the final y is 1.
  - A4 returns 1 or 2.
  - Outcomes: 1 1 1 and 1 2 1.

**Case a = 3** (A1 after B2, with B3 before A2)
- The reasoning is the same as for a = 1, with 3 in place of 1.
- Outcomes: 3 3 3, 3 3 0, 3 2 0, 3 0 0 and 3 2 3.

BEGIN
0 0 0
0 2 0
1 1 1
1 1 0
1 2 0
1 0 0
1 2 1
3 3 3
3 3 0
3 2 0
3 0 0
3 2 3
END