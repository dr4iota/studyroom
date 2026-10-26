All 12 combinations of (Q1, Q2, Q3) are possible. With no sync points, the only constraints are that each thread's operations keep their order and that any interleaving of the two threads is allowed.

- **Q1** is 4 if B2 (write 4 to y) takes effect before A1, and 0 otherwise. B1 always returns 0 because it precedes B2 in B's order.
- **Q2** is the value of the latest A-write to x before B3. B5 always comes after B3, so it doesn't matter here. The possible values are 0 (before A2), 2 (after A2 but before A3, or after A5), and 4 (after A3 but before A5).
- **Q3** is 2 if A5 comes after B5, and 4 if B5 comes after A5. The earlier A-writes are overwritten by A5 in either case.

Each Q1 value can be combined with each Q2 value and each Q3 value through a suitable interleaving. For example, `A1 B1 B2 B3 B4 B5 A2 A3 A4 A5` gives 0 0 2, and `B1 B2 A1 A2 A3 B3 A4 A5 B4 B5` gives 4 4 4.

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