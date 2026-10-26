The three asked reads and the final value of x depend only on the operations that touch x: A4 (write 5), B1 (write 4), C4 (write 1), plus the reads A5 and C5. The z and y operations don't affect these values, so they can be ignored.

Each operation takes effect atomically, so an execution is a total order of the five x-operations that respects program order: A4 before A5, and C4 before C5. B1 can go anywhere. That gives 30 orders. For each one:
- A5 returns the latest x-write before A5 (A4 always qualifies).
- C5 returns the latest x-write before C5 (C4 always qualifies).
- The final x is the latest x-write overall.

Enumerating all 30 orders gives 14 distinct outcomes. For example, C4 A4 A5 C5 with B1 placed first gives (5,5,5), and C4 C5 A4 A5 with B1 between C5 and A4 gives (5,1,5). Combinations such as (1,5,4) and (4,5,1) cannot occur, because they would require contradictory orderings of C4 and A4.

Q1 is A5's value, Q2 is C5's value, Q3 is the final x.

BEGIN
1 1 1
1 1 4
1 4 4
4 1 1
4 1 4
4 4 4
4 5 4
5 1 1
5 1 4
5 1 5
5 4 4
5 4 5
5 5 4
5 5 5
END