Every operation takes effect at a single instant, and each thread's operations keep their listed order. So the executions are exactly the interleavings of the two sequences.

**Final value of x.** The last write is either A5 (final 2) or B4 (final = the value B2 read).

**Case 1: B4 takes effect before A5.**
- B1, B2 and B3 all precede B4, so they precede A5 and cannot see 2.
- They see x in the order 0, 3, 1. A4's write comes after B4, which comes after B3, so B cannot see it either.
- So (B1, B3) ∈ {(0,0), (0,3), (0,1), (3,3), (3,1), (1,1)}, with final value 2.
- All of these are achievable.

**Case 2: B4 takes effect after A5.**
- No B4 write can occur before A3, so A3 reads 1 and A4 writes 1.
- The timeline of x is therefore 0, 3, 1, 2.
- B1, B2 and B3 read non-decreasing positions on this timeline.
- The final value is B2's value, so b1 ≤ b2 ≤ b3 in the order 0 < 3 < 1 < 2.
- Any such triple is achievable.

**Combining the cases** (Q1 = B1, Q2 = B3, Q3 = final x). For each (b1, b3), the possible finals are every value between them in the order 0, 3, 1, 2, plus 2 from Case 1 when b3 ≠ 2.

BEGIN
0 0 0
0 0 2
0 3 0
0 3 3
0 3 2
0 1 0
0 1 3
0 1 1
0 1 2
0 2 0
0 2 3
0 2 1
0 2 2
3 3 3
3 3 2
3 1 3
3 1 1
3 1 2
3 2 3
3 2 1
3 2 2
1 1 1
1 1 2
1 2 1
1 2 2
2 2 2
END