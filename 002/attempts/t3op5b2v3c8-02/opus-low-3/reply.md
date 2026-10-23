**Values each read can return**

- **A1 (Q1):** Before A1, only B2 (writes 1) and C1 (writes 2) can have written x. A5 comes after A1 in thread A. So A1 returns 0, 1 or 2. It can never return 3.
- **B4 (Q2):** B4 comes after B3, so it sees B3 or a later write to y:
  - B3 or C3 gives 1.
  - C2 gives 2, if C2 takes effect after B3.
  - A4 gives 3.
  - A3 gives the value read by A1.
  - C5 gives the value read by C4.
- **C4 (Q3):** C4 comes after C2 and C3 in thread C. So C2's value 2 can only reach C4 through a copy. C4 sees one of these:
  - C3 or B3 gives 1.
  - A4 gives 3.
  - A3 gives the value read by A1.
  - B5 gives the value read by B4.
- **The two copies cannot both happen.** B4 cannot read C5 while C4 reads B5. That would need B4 < B5 < C4 < C5 < B4, which is a cycle.

**Combinations**

Let a be A1's value. Then B4 ∈ {1, 2, 3, a}, and C4 ∈ {1, 3, a, B4}. Every such pair can be produced by some interleaving. For example, (0, 2, 0) happens with this order: A1 reads x before B2 and C1, then B3, C2, B4, C3, A3, C4.

- **a = 0:** B4 ∈ {0, 1, 2, 3}, giving 13 combinations.
- **a = 1:** B4 ∈ {1, 2, 3}, giving 7 combinations.
- **a = 2:** B4 ∈ {1, 2, 3}, and C4 ∈ {1, 2, 3} in every case, giving 9 combinations.

That is 29 combinations in total.

BEGIN
0 0 0
0 0 1
0 0 3
0 1 0
0 1 1
0 1 3
0 2 0
0 2 1
0 2 2
0 2 3
0 3 0
0 3 1
0 3 3
1 1 1
1 1 3
1 2 1
1 2 2
1 2 3
1 3 1
1 3 3
2 1 1
2 1 2
2 1 3
2 2 1
2 2 2
2 2 3
2 3 1
2 3 2
2 3 3
END