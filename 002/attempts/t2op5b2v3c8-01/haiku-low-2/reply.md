Each thread's operations take effect in program order, and with no sync points any interleaving of the two threads is achievable. Let a3 be the value A3 reads, and define the values as follows:

- **b1 and b2** are reads of x made before any B write to x, so they can only see A's writes (0, 3, or 1). Since B1 precedes B2, their phases are non-decreasing, which leaves six pairs: (0,0), (0,3), (0,1), (3,3), (3,1), (1,1).
- **a3** is 1 if no B write lands between A2 and A3. It is b1 if B3 lands between A2 and A3 and B4 does not. It is b2 if B4 lands between A2 and A3.
- **Final y** is a3, since A4 is the only write to y and always executes.

Working through the three cases for a3 and checking each (b1, b2) pair for feasibility gives these twelve outcomes (b1 b2 y):

- a3 = 1: (0,0,1), (0,1,1), (0,3,1), (3,1,1), (3,3,1), (1,1,1)
- a3 = b1: (0,0,0), (0,1,0), (0,3,0), (1,1,1), (3,1,3), (3,3,3)
- a3 = b2: (0,0,0), (0,1,1), (0,3,3), (1,1,1), (3,1,1), (3,3,3)

Their union is the set below.

BEGIN
0 0 0
0 0 1
0 1 0
0 1 1
0 3 0
0 3 1
0 3 3
1 1 1
3 1 1
3 1 3
3 3 1
3 3 3
END