The three reads can return these combinations of values for Q1 (A2), Q2 (A4), and Q3 (B1).

**Why the values are limited:**
- A's only write, A5, comes after A2 and A4, so A2 and A4 can only see writes from B.
- B's writes in order are B2=1, B3=2, B4=3, B5=1. Before any of them, the value is 0. So the possible values are 0, 1, 2, 3.
- If A2 sees the first k of B's writes and A4 sees the first m of them, then k ≤ m. Every such pair (k, m) can be realized by some interleaving. This gives 12 distinct (Q1, Q2) pairs. For example, (1,0) and (3,2) are impossible because a later read can't see an earlier prefix of writes.
- B1 is B's first operation, so it sees only A5 (value 1) or nothing (value 0). It can return 1 only if A5 takes effect before B1. In that case A5 is after both A2 and A4, and B's writes are all after B1, so A2 and A4 both return 0. So Q3=1 is possible only with (Q1, Q2) = (0, 0).
- Q3=0 is possible with every (Q1, Q2) pair, by placing B1 first.

That gives 13 combinations.

BEGIN
0 0 0
0 0 1
0 1 0
0 2 0
0 3 0
1 1 0
1 2 0
1 3 0
2 2 0
2 3 0
2 1 0
3 3 0
3 1 0
END