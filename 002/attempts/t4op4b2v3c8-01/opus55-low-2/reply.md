All 27 combinations are possible: A3, C2 and the final y can each independently be 0, 1 or 3.

**Values each read can return**

There are no sync points, so any interleaving that keeps each thread's order is allowed.

- **Values x can hold.** x is written by:
  - B1, which writes 1.
  - D1, which writes 3.
  - A2 and A4, which write the value A1 read.
  - C3, which writes the value C2 read.
  
  x starts at 0. So x only ever holds 0, 1 or 3, and A3 and C2 can each only return one of these.
- **Values the final y can be.** y is written by C1 (1), D2 (1) and B3, which writes whatever B2 read. B2 always comes after B1, but it can still read:
  - 0, if A1 read 0 and A2 writes 0 after B1 (or C3 writes 0 after B1).
  - 1, straight after B1.
  - 3, after D1.
  
  If B3 is the last write to y, the final y is B2's value (0, 1 or 3). Otherwise it is 1.

**Every combination can occur together**

Each read can take its value in a separate time window, and these windows can be arranged around each other.

- C2 reads 0 if it runs before any write, 1 if it runs after B1, or 3 if it runs after D1.
- A3 reads 0 just after A2 writes 0, 1 after B1 or after C3 writes 1, or 3 after D1.
- B2 reads its value in its own window, and B3 is placed after C1 and D2 so it is the last write to y.

Example for one of the tighter cases, A3=3, C2=0, y=0:
1. C1 writes 1 to y.
2. C2 reads 0.
3. A1 reads 0.
4. B1 writes 1 to x.
5. A2 writes 0 to x.
6. B2 reads 0.
7. D1 writes 3 to x.
8. A3 reads 3.
9. D2 writes 1 to y.
10. B3 writes 0 to y, the last write to y.

The other steps go anywhere afterwards. The remaining combinations can be built the same way.

BEGIN
0 0 0
0 0 1
0 0 3
0 1 0
0 1 1
0 1 3
0 3 0
0 3 1
0 3 3
1 0 0
1 0 1
1 0 3
1 1 0
1 1 1
1 1 3
1 3 0
1 3 1
1 3 3
3 0 0
3 0 1
3 0 3
3 1 0
3 1 1
3 1 3
3 3 0
3 3 1
3 3 3
END