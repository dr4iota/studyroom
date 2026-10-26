Let a be the value A1 reads from x. It can be 0 (A1 before C1) or 1 (A1 after C1 or C4).

- **B2 (Q1)** reads z. It returns 0, the value a (after A2), or 3 (after C3).
- **C2 (Q2)** reads y. It returns 0, 2 (after B1), 3 (after A4) or a (after A5).
- **Final y (Q3)** is a if A5 is the last write to y. It is 2 if B1 comes after A5.

**Case a = 0 (A1 before C1).** B2 ∈ {0,3}, C2 ∈ {0,2,3}, final y ∈ {0,2}. All 12 combinations are possible. Two example orders:
- `A1,C1,C2,B1,C3,B2,A2,A3,A4,A5` gives 3 0 0.
- `A1,A2,A3,A4,C1,C2,A5,B1,C3,B2` gives 3 3 2.

**Case a = 1.** B2 ∈ {0,1,3}, final y ∈ {1,2}.
- **C2 = 1:** A5 comes before C2, so A1 read the 1 from C1. B2 can be 0, 1 or 3 and final y can be 1 or 2. All 6 combinations are possible.
- **C2 = 0:** C2 comes before B1 and A4. All 6 combinations are possible.
- **C2 = 2 or C2 = 3:**
  - If final y = 2, B1 comes after A5. B2 comes after B1, so B2 is also after A2, and B2 = 0 is impossible.
  - If final y = 1, B2 can be 0, 1 or 3.
  - That gives B2/y pairs 0 1, 1 1, 3 1, 1 2 and 3 2 for each of these C2 values.

BEGIN
0 0 0
0 0 2
0 2 0
0 2 2
0 3 0
0 3 2
3 0 0
3 0 2
3 2 0
3 2 2
3 3 0
3 3 2
0 1 1
0 1 2
1 1 1
1 1 2
3 1 1
3 1 2
0 0 1
1 0 1
1 0 2
3 0 1
0 2 1
1 2 1
3 2 1
1 2 2
0 3 1
1 3 1
3 3 1
1 3 2
END