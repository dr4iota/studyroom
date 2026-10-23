The answer is 13 possible combinations of (Q1, Q2).

**Approach.** Each thread runs its operations sequentially, so every execution is an interleaving of the two threads' atomic operations. Thread A's writes take effect in the order 2, 3, 1, 3 (A1–A4), and A5 always follows A4. Each B read sees the last A write before it, because B4 and B5 come after B3.

**Q2 (value of B3).** Let p3 be the number of A writes (A1–A4) that take effect before B3. The value is 0 if p3 = 0, 2 if p3 = 1, 3 if p3 = 2, 1 if p3 = 3, and 3 if p3 = 4.

**Q1 (value of A5).** A5 sees A4's value, 3, unless B4 or B5 takes effect between A4 and A5. In that case it sees v, the value B2 read, since B4 and B5 both write v. B2 read a prefix of A's writes with p2 ≤ p3, so v must come from a prefix no longer than the one B3 saw.

**Combinations.**
- Q1 = 3 (no B write between A4 and A5) is achievable for every Q2 value 0, 1, 2, 3.
- Q1 = v requires a B write between A4 and A5:
  - If B3 is after A4 (p3 = 4, Q2 = 3), v can be 0, 1, 2 or 3.
  - If B3 is before A4 (p3 ≤ 3), v is any value from a prefix p2 ≤ p3:
    - Q2 = 0: v = 0.
    - Q2 = 2: v ∈ {0, 2}.
    - Q2 = 3 (p3 = 2): v ∈ {0, 2, 3}.
    - Q2 = 1 (p3 = 3): v ∈ {0, 1, 2, 3}.

Collecting these gives 13 distinct pairs.

BEGIN
0 0
3 0
0 1
1 1
2 1
3 1
0 2
2 2
3 2
0 3
1 3
2 3
3 3
END