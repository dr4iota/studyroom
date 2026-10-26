Thread B is the only writer of y, and it writes 2, 2, 1 in that order, so y over time goes 0, 2, 2, 1. Thread A's two y reads therefore see a non-decreasing position in that sequence.

**Q1 and Q2 (A2, A4).** A2 happens before A4, so the possible pairs are (0,0), (0,2), (0,1), (2,2), (2,1) and (1,1).

Nothing links y to the x constraints. Thread B can run any number of its steps between A1 and A2, or between A2 and A4. Even A1 = 0 followed by A2 = 1 is possible.

**Q3 (final x).** Threads A and B both write x. B writes only 2. A writes the value A1 read, which is either 0 or 2.
- A3 returned 2, so B1 took effect before A3.
- A1 could have read 0 if it ran before B1.
- If A1 read 2, A5 to A7 all write 2, so the final x is 2.
- If A1 read 0, A5 to A7 write 0 after A3. The final x is 0 if B3 took effect before A5. It is 2 if B3 took effect after A7.

So the final x can be 0 or 2, and either value combines with every (A2, A4) pair.

BEGIN
0 0 0
0 0 2
0 2 0
0 2 2
0 1 0
0 1 2
2 2 0
2 2 2
2 1 0
2 1 2
1 1 0
1 1 2
END