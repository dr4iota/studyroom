These are all the possible combinations. Block x is never written, so B2 always returns 0 and rules nothing out. There are no sync points, so every interleaving that keeps each thread's order is allowed. The order is A1 (write 3), A2 (read), A3 (write 4), A4 (write 3) in thread A, and B3 (read), B4 (write 1), B5 (write 2) in thread B.

**Case A2 = 3:** neither B4 nor B5 takes effect between A1 and A2.
- If B4 and B5 both come after A2, B3 can come before A1 and return 0. It can come between A1 and A3 and return 3, or between A3 and A4 and return 4.
- If B5 comes after A4 the final y is 2; otherwise A4 writes last and it is 3. Every value of B3 can go with either final value.
- So all of 3/{0,3,4}/{2,3} are possible.

**Case A2 = 1:** B4 takes effect between A1 and A2, and B5 takes effect after A2.
- B3 comes before B4, so it returns 0 (before A1) or 3 (after A1).
- B5 can come after A4, giving final 2, or before A4, giving final 3.

**Case A2 = 2:** B5 takes effect between A1 and A2.
- B3 returns 0 or 3, as in the previous case.
- A3 and A4 come after B5, so the final y is always 3.

BEGIN
3 0 2
3 0 3
3 3 2
3 3 3
3 4 2
3 4 3
1 0 2
1 0 3
1 3 2
1 3 3
2 0 3
2 3 3
END