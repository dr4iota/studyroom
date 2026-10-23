Because no sync points are given, every interleaving that keeps each thread's own order is allowed. B1 returning 0 only requires B1 to precede B2, which is always possible.

**Q1 (A1):** A1 reads y, which is 0 until B2 writes 4. A1 can run before B2 and return 0, or after B2 and return 4. So Q1 is 0 or 4.

**Q2 (B3):** B3 comes after B2 and before B5, so it sees only A's writes to x.
- It returns 0 if it runs before A2.
- It returns 2 if A2 has run but A3 has not.
- It returns 4 if A3 has run but A5 has not.

None of these choices depends on whether A1 ran before or after B2. For Q1 = 0, A1 runs first, then B1, B2, B3, and the rest of A follows. For Q1 = 4, A1 simply runs after B2.

**Q3 (final x):** The last write to x is either A5 (2) or B5 (4), and both orders are possible for every case above.
- B5 can follow all of A, giving 4.
- A5 can follow B5, giving 2. A5 is A's last step, so it can always be delayed past B5. The exception is B3 = 4, where A5 must stay after B3 anyway, which is still fine.

This gives every combination of Q1 ∈ {0, 4}, Q2 ∈ {0, 2, 4} and Q3 ∈ {2, 4}.

BEGIN
0 0 2
0 0 4
0 2 2
0 2 4
0 4 2
0 4 4
4 0 2
4 0 4
4 2 2
4 2 4
4 4 2
4 4 4
END