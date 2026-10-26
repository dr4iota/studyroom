Final x can't be 3, so every combination ends in 1 or 2.

**Constraints that apply**
- C1 reads 0, so C1 takes effect before every write to y. The writes to y are A1 and B3, and both write 1.
- Every thread's operations take effect in program order.
- C2 ends before P, and B4 comes after P.
- C4 ends before Q.
- B1 ends before R.

**Q1 (A2)**
- A2 comes after A1, which comes after C1.
- A2 can read 0 if it runs before any write to x.
- A2 can read 1 when D2 is the latest write before it.
- A2 can read 2 when C2, B1 or C4 is the latest write.
- A2 can read 3 when D1 or C3 is the latest write.
- So A2 can be 0, 1, 2 or 3.

**Q2 (D3)**
- D3 reads 0 if it runs before A1 and B3.
- D3 reads 1 if it runs after either of them.
- So D3 can be 0 or 1.
- If D3 reads 0, D1 and D2 have already run before A1, and therefore before A2. A2 then cannot read 0.
- With D3 = 0, A2 can still read 1 (D2 is the latest write), 2 (C2, B1 or C4 is later) or 3 (C3 is later).

**Q3 (final x)**
- D1 is followed by D2, so D1 is never last.
- C3 is followed by C4, so C3 is never last.
- So the final value cannot be 3.
- The final value is 1 if D4 is last. That is consistent with every other constraint.
- The final value is 2 if B1 or C4 comes after D4. That is also consistent with every other constraint.

**Combining**
- A2 = 0 requires D3 = 1, giving 2 combinations with final 1 or 2.
- A2 = 1, 2 or 3 works with either D3 value and either final value, giving 12 combinations.

BEGIN
0 1 1
0 1 2
1 0 1
1 0 2
1 1 1
1 1 2
2 0 1
2 0 2
2 1 1
2 1 2
3 0 1
3 0 2
3 1 1
3 1 2
END