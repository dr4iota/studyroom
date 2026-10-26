The final value of z is the value of whichever write to z takes effect last. The writes to z are B1 (4), B2 (2), B3 (5), and C2 (1).

- Thread B runs B1, B2, B3 in order, so B1 and B2 always take effect before B3. Neither can be last, which rules out 4 and 2.
- B3 (5) is last if C2 takes effect before B3, which is allowed since C2 can run at any point.
- C2 (1) is last if it takes effect after B3, which is also allowed. The reads and writes on x and y don't constrain the order of writes to z.

So the possible final values are 1 and 5.

BEGIN
1
5
END