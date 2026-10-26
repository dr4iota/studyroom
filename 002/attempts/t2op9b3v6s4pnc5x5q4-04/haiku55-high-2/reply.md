**Key facts from the constraints**

- **Writes to y:** only A8 writes y, and it writes the value A7 read. A7 always reads A6's write, which copies A4's value `v`, so A8 writes `v` and **final y = v**.
- **Writes to z:** B8 always comes after every other z-write (A9 < R < B8), so **final z = Q1**. B9 comes right after B8 and reads it, so **Q1 = Q4 = value read by B2 = b**.
- **B2 (reads y):** it returns `v` if A8 happened before B2, otherwise 0. So **b ∈ {0, v}**.
- **A4 (reads z):** A1 and B1 are both before A4, so **v ∈ {1, 6}**. v = 6 if A1 is after B1, and v = 1 if A1 is before B1.
- **Final x:** B7 is always after B5 and B6, so the last x-write is either B7 (value 4) or A2 (value 1). **Final x ∈ {1, 4}**.
- **Coupling:** if A2 is after B7, then B2 < B7 < A2 < A8, which forces b = 0.

**Feasible (b, v, x) combinations.** Each was checked by building an explicit order:

- x = 1 (forces b = 0): v = 6 and v = 1 both work.
- x = 4: (b, v) = (0, 6), (0, 1), (6, 6), (1, 1) all work.

**Outcomes** (Q1, Q2, Q3, Q4) = (b, x, v, b):

- (0, 1, 6, 0)
- (0, 1, 1, 0)
- (0, 4, 6, 0)
- (0, 4, 1, 0)
- (6, 4, 6, 6)
- (1, 4, 1, 1)

BEGIN
0 1 6 0
0 1 1 0
0 4 6 0
0 4 1 0
6 4 6 6
1 4 1 1
END