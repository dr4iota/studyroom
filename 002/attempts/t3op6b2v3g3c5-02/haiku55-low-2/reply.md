The possible outcomes are 12 combinations. Q1 is always 0, Q2 can be 0, 2, or 3, and Q3 can be 0, 1, 2, or 3, with every pairing of Q2 and Q3 achievable.

**Key facts**

- **Q1 is always 0.** Block x is only written by A3 (value a1) and B3 (value b1). A1 reads x before A3 and B3 can only be seen by A1 if B3 precedes it, and B1 reads x before B3. Working through the cases (A3 before B1, or B3 before A1, or neither) forces a1 = b1 = 0.
- **B4 = 0 holds automatically**, since every write to x is 0.
- **Q2 (B2's read) cannot be 1.** The only write of 1 is B5, which comes after B2. The only other way to get a 1 into y before B2 is C4 or C6 writing c3 = 1, but that requires B5 before C3, which is before C4, which is before B2, while B2 precedes B5. That is a cycle, so 1 is impossible. The values 0, 2 and 3 are each achievable (e.g. B2 before C1 gives 0; C1 last before B2 gives 2; A4 last before B2 gives 3).
- **Q3 (C3's read) can be 0, 1, 2 or 3.** The last write before C3 is C1 (2), A4 (3), A5 (0) or B5 (1), and each can be the last one while A2 still reads 2. For example, C1,A1,A2,A3,A4,A5,B1..B5,C2,C3 gives 1; the same prefix ending at A4 with C2,C3 gives 3; ending at A5 gives 0; and C1,C2,C3 first gives 2.
- **Every (Q2, Q3) pair with Q2 ∈ {0,2,3} and Q3 ∈ {0,1,2,3} has a witnessing schedule.** For example, Q2 = 3 with Q3 = 2 uses C1,C2,C3,A1,A2,A3,A4,B1,B2,B3,B4,A5,B5,C4,C5,C6.

BEGIN
0 0 0
0 0 1
0 0 2
0 0 3
0 2 0
0 2 1
0 2 2
0 2 3
0 3 0
0 3 1
0 3 2
0 3 3
END