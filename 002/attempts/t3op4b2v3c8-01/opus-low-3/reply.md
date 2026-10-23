Every combination is possible except two: Q3 can never be 3, and when Q3 = 2 with Q2 = 0, Q1 must be 0. That gives 17 combinations.

**Values that can appear in y**

- y starts at 0.
- B2 writes 2.
- C4 writes the value C3 read from x. That value is 0 (the initial value), 3 (from B1), or whatever A3 wrote.
- A3 writes the value A2 read from y.
- So y only ever holds 0, 2 or 3.

**Q3 (C1)**

- The only write of 3 to y is C4, and C4 comes after C1 in thread C.
- So C1 returns 0 (before B2) or 2 (after B2), never 3.

**Case C1 = 2**

- C1 is after B2, so C3 is after B1. C3 therefore reads 3 or A3's value, and C4 writes 3, 0 or 2.
- **B3 = 2:** B3 runs before C4 or C4 writes 2. A1 can be 0 (before B2), 2, or 3 (after C4 writes 3). All three work.
- **B3 = 3:** C4 writes 3 before B3. A1 can be 0, 2 or 3.
- **B3 = 0:** C4 must write 0, so C3 must read 0 from x.
  - C3 is after B1, so x = 0 requires A3 to have written 0 after B1.
  - A2 cannot read 0 after C4, because C4 depends on A3, which comes after A2. So A2 read 0 before B2.
  - A1 comes before A2, so A1 = 0 is the only option.

**Case C1 = 0**

- C1 runs before B2. C3 can read x before B1 and before A3, so C4 can write 0, 3 or 2.
- **B3 = 2:** A1 can be 0, 2 or 3. For 3, C4 writes 3, A1 reads it, then B2 writes 2 before B3.
- **B3 = 3:** C4 writes 3 after B2 and before B3. A1 can be 0, 2 or 3.
- **B3 = 0:** C4 writes 0 after B2, so 3 is never written to y. A1 can be 0 or 2.

BEGIN
0 2 2
2 2 2
3 2 2
0 3 2
2 3 2
3 3 2
0 0 2
0 2 0
2 2 0
3 2 0
0 3 0
2 3 0
3 3 0
0 0 0
2 0 0
0 2 0
2 2 0
END