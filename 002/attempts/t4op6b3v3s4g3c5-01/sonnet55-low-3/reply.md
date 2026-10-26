Possible outcomes are listed below; the constraint analysis follows.

**Constraints on x (Q3).**
- A6 reads 0 and happens after A5 ends, which is after R.
- The chain C3 < C4 < C5 start < Q < D1 < R < A5 end < A6 forces C3's write of 1 to take effect before A6.
- So the last write to x before A6 must be a 0. The only 0 write that can fit is C5's, so C1 read y = 0 and C5 writes 0.
- C5's write therefore takes effect after every other x-write that precedes A6. C2 also writes 0.
- B2 and B4 occur before D1, because B5 must precede D1 reading 2. D3 occurs after D1.
- If D3 takes effect after C5, the final x is 3. If D3 takes effect before C5 and nothing follows, the final x is 0. B4's 3 can never be the last write, because D3 or C5 comes later.
- The final x is therefore 0 or 3.

**Possible values of A2.**
- A2 is before P, so it can read 0, 3 (from B1 or D2) or 2 (from B3).
- It cannot read 1, because A4 comes after A2 and D5 starts after P.

**Possible values of A3.**
- A3 comes after A2 and is not forced to be before or after P.
- It can read 0 (only if A2 read 0), 3 (B1 or D2), 2 (B3) or 1 (D5, which starts after P).
- Once A2 has read a nonzero value, A3 cannot read 0.

**Combinations of (A2, A3).**
- A2 = 0: A3 can be 0, 1, 2 or 3.
- A2 = 2: A3 can be 1, 2 or 3.
- A2 = 3: A3 can be 1, 2 or 3.

Each of these ten pairs can occur with a final x of 0 or 3, giving 20 combinations.

BEGIN
0 0 0
0 0 3
0 1 0
0 1 3
0 2 0
0 2 3
0 3 0
0 3 3
2 1 0
2 1 3
2 2 0
2 2 3
2 3 0
2 3 3
3 1 0
3 1 3
3 2 0
3 2 3
3 3 0
3 3 3
END