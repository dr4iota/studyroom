An execution is valid if it respects each thread's program order. There are no sync points in this problem.

**Key variable.** Let a be the value returned by A1. A1 reads x, and the only writes to x before it can be C1 or C4, which both write 1. So a ∈ {0, 1}.

- a = 0 requires A1 to take effect before C1. C1 is before C2, C3 and C4 in thread C, so A1 is before all of C's operations.
- a = 1 requires A1 to take effect after C1.

**What each asked value can be:**
- **B2** reads z. The writes to z are A2 (writes a) and C3 (writes 3). So B2 ∈ {0, a, 3}.
- **C2** reads y. The writes to y are B1 (2), A4 (3) and A5 (a). So C2 ∈ {0, 2, 3, a}.
- **Final y** is set by the last of B1, A4 and A5. A5 always follows A4, so final y ∈ {a, 2}.

**Case a = 0**

Here B2 ∈ {0, 3}, C2 ∈ {0, 2, 3} and final y ∈ {0, 2}. A1 comes first, and the remaining operations can be arranged to give any of these 2 × 3 × 2 = 12 combinations. Two examples:
- B2 = 3, C2 = 2, y = 0: A1, C1, A2, A3, A4, B1, C2, C3, B2, A5.
- B2 = 0, C2 = 3, y = 2: A1, A2, A3, A4, C1, C2, B1, B2, C3, A5, C4, B3, B4.

**Case a = 1, final y = 1**

Final y = 1 means A5 is the last write to y, so B1 comes before A5. Here B2 ∈ {0, 1, 3} and C2 ∈ {0, 1, 2, 3}, and all 12 combinations are possible. Examples:
- B2 = 0, C2 = 3: C1, B1, B2, A1, A2, A3, A4, C2, C3, A5.
- B2 = 0, C2 = 1: C1, B1, B2, A1, A2, A3, A4, A5, C2, C3.

**Case a = 1, final y = 2**

Final y = 2 means B1 comes after A5. B2 follows B1 in thread B, so B2 is also after A2. That leaves z holding 1 or 3 when B2 runs, so B2 cannot return 0. B2 ∈ {1, 3} combines with every C2 ∈ {0, 1, 2, 3}, giving 8 combinations. Examples:
- B2 = 1, C2 = 0: C1, C2, C3, A1, A2, A3, A4, A5, B1, B2.
- B2 = 3: same as above, but with C3 placed after A2 and before B2.

**Union of the cases**

| Final y | B2 | Possible C2 |
|---|---|---|
| 0 | 0 or 3 | 0, 2, 3 |
| 1 | 0, 1 or 3 | 0, 1, 2, 3 |
| 2 | 0 | 0, 2, 3 |
| 2 | 1 or 3 | 0, 1, 2, 3 |

BEGIN
0 0 0
0 2 0
0 3 0
3 0 0
3 2 0
3 3 0
0 0 1
0 1 1
0 2 1
0 3 1
1 0 1
1 1 1
1 2 1
1 3 1
3 0 1
3 1 1
3 2 1
3 3 1
0 0 2
0 2 2
0 3 2
1 0 2
1 1 2
1 2 2
1 3 2
3 0 2
3 1 2
3 2 2
3 3 2
END