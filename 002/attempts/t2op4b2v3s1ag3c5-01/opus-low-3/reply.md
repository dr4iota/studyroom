Each case below follows from the rules.

**What is fixed by the sync point P**
- A1, A2 and A3 happen before P, so A2's write of 2 to y happens before P.
- B1 and B2 happen before P.
- A4 starts before P and ends after P. Its read can take effect on either side of P.
- B3 also spans P. Its write of 3 to y can take effect on either side of P.
- B4 happens entirely after P, so it comes after both A2 and B3.

**Q3 (final value of y)**
- B4 is the last write to y, and it writes what B1 read.
- B1 can read x as 0 (before A1), 3 (between A1 and A3) or 1 (after A3).
- So the final y is 0, 3 or 1, matching B1.

**Q2 (value returned by B2)**
- B3 and B4 come after B2, so the only write B2 can see is A2's 2.
- B2 returns 2 if A2 took effect first, otherwise 0.
- If B1 returned 1, B1 came after A3 and so after A2. B2 comes after B1, so in that case B2 must return 2.
- If B1 returned 0 or 3, B2 can still take effect before A2, so B2 can be 0 or 2.

**Q1 (value returned by A4)**
- A4 returns 2 if its read takes effect before B3's write.
- It returns 3 if its read falls between B3's write and B4's write.
- A4 can end after B4, because both only need to end after P. So A4 can also return B4's value, which is B1's value.
- None of these choices conflicts with the choices for Q2.

**Combining**
- Final y = 0: A4 ∈ {2, 3, 0}, B2 ∈ {0, 2}.
- Final y = 3: A4 ∈ {2, 3}, B2 ∈ {0, 2}.
- Final y = 1: A4 ∈ {2, 3, 1}, B2 = 2.

BEGIN
2 0 0
2 2 0
3 0 0
3 2 0
0 0 0
0 2 0
2 0 3
2 2 3
3 0 3
3 2 3
2 2 1
3 2 1
1 2 1
END