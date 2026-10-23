Q1 is the value A5 returns, and Q2 is the value B3 returns.

**Key facts:**
- A5 is A's last operation. Its value is the last write before it: A4 writes 3, unless a B write (B4 or B5, both writing B2's value r2) falls between A4 and A5. So A5 ∈ {3, r2}.
- B3 comes before B4 and B5, so no B write can precede it. Its value is the last A write before it, or 0. Any slot among A's writes is reachable, so r3 ∈ {0, 1, 2, 3}.
- r2 (B2's value) depends on where B2 falls among A's writes: 0 (before A1), 2 (between A1 and A2), 3 (between A2 and A3), 1 (between A3 and A4), or 3 (after A4).

**Joint constraints:**
- **A5 = 0:** requires r2 = 0, so B2 is before A1. B3 comes after B2 and can fall in any slot, so r3 ∈ {0, 1, 2, 3}.
- **A5 = 3:** B4 and B5 can both sit after A5, so B3 is unconstrained. r3 ∈ {0, 1, 2, 3}.
- **A5 = 2:** requires r2 = 2, so B2 is between A1 and A2. B3 must come after B2, which rules out r3 = 0. r3 ∈ {1, 2, 3}.
- **A5 = 1:** requires r2 = 1, so B2 is between A3 and A4. B3 must come after B2, which leaves only r3 ∈ {1, 3}.

This gives 13 combinations.

BEGIN
0 0
0 1
0 2
0 3
1 1
1 3
2 1
2 2
2 3
3 0
3 1
3 2
3 3
END