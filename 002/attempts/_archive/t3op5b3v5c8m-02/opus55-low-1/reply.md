**Approach:** there are no sync points, so any interleaving that respects each thread's own order is allowed. I first find the possible values for each asked item separately, then check which combinations can happen together.

**Q2 (B3, read of y).** B3 comes after B2, which writes 1 to y. The other writes to y are A1 (4) and A2 (1).
- B3 returns 1 if the last write to y before it is B2 or A2.
- B3 returns 4 if the order is B2 < A1 < B3 < A2.
- So B3 ∈ {1, 4}. B4 then writes that value to x.

**Q1 (A3, read of x).** The writes to x are C2 (2), C3 (1) and B4 (the value of B3). A3 can also run before any of them.
- A3 = 0: A3 runs before C2 and B4.
- A3 = 2: the last write before A3 is C2.
- A3 = 1: the last write before A3 is C3, or B4 when B3 = 1.
- A3 = 4: only when B3 = 4 and B4 is the last write to x before A3.

**Q3 (final z).** The writes to z are B1 (4), A4 (the value of A3), C4 (the value of C1) and C5 (4).
- C4 always comes before C5, so C4 can never be the final write.
- The final write is therefore B1 or C5 (value 4), or A4 (value of A3).
- Final z ∈ {4, A3}.

**Checking the combinations.**
- **Final z = A3:** A4 is the last operation of thread A. It can always be placed after every other operation, so this works for any reachable pair (A3, B3).
- **Final z = 4:** let C5 run after A4.
- **B3 = 4 with each A3 value:** this needs B2 < A1 < B3 < A2 < A3. That still leaves room for A3 to come before C2 and B4 (giving 0), or after C2, C3 or B4 as needed (giving 2, 1 or 4).
- **B3 = 1 with A3 = 4:** impossible, because nothing writes 4 to x in that case.

BEGIN
0 1 0
0 1 4
1 1 1
1 1 4
2 1 2
2 1 4
0 4 0
0 4 4
1 4 1
1 4 4
2 4 2
2 4 4
4 4 4
END