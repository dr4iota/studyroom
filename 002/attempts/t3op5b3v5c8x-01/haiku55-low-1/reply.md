The asked values are Q1 = B5's read, Q2 = C4's read, and Q3 = the final y. There are 21 possible combinations.

**Setup.** Each thread's operations are sequential, but operations of different threads can interleave freely. So the possible outcomes are those of all interleavings that respect each thread's order.

**Key facts:**
- Only A2 and A3 write A1's value (call it a), and a ∈ {0, 1, 2}, since A1 reads z before A2 and A3.
- C3 and C5 always read x = 1, since C2 precedes them in C's thread.
- B2 reads x = 1 if C2 happens before it, and 0 otherwise.
- The final y is a (from A4) if A4 happens after B3, and B2's value if B3 happens after A4.
- The z-writes are B1 (1), C1 (2), A2 (a), and A3 (a).

**Constraints that rule out some triples:**
- If B5 returns 0, then a = 0. If C4 returns 0, then a = 0.
- If a = 0, then B5 returns 2 only via C1, and C4 returns 1 only via B1. Those two cannot hold together, since C4 follows C1.
- Final y = 2 requires a = 2.
- (B5, C4, final y) = (2, 0, 1) is impossible. It would need a = 0, and final y = 1 would need A3 before B5, forcing both A-writes before C1, which leaves no way for C4 to read 0.

**Feasibility.** I checked each candidate triple by constructing an explicit interleaving. Among the candidates allowed by the rules above, these 21 are achievable, and every other candidate is ruled out by the constraints.

BEGIN
0 0 0
0 0 1
0 1 0
0 1 1
0 2 0
0 2 1
1 0 0
1 0 1
1 1 0
1 1 1
1 1 2
1 2 0
1 2 1
1 2 2
2 0 0
2 1 0
2 1 1
2 1 2
2 2 0
2 2 1
2 2 2
END