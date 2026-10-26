Only the operations on x matter for these questions. The operations on y and z impose no ordering on x, so the only constraints are program order within each thread.

- The writes to x are A4 (5), B1 (4) and C4 (1).
- A5 must come after A4, and C5 must come after C4.
- Reads A5 and C5 do not affect x, so each can be placed independently anywhere after its own thread's write.
- The final value of x is the last of the three writes in the chosen order.

For each of the 6 orders of the three writes, A5 can return the value of any write from A4's position onward, and C5 can return the value of any write from C4's position onward. Taking the union over all orders gives:

- Final x = 1: (A5, C5) = (5,1), (4,1), (1,1)
- Final x = 4: (5,1), (5,4), (1,1), (1,4), (4,1), (4,4), (5,5), (4,5)
- Final x = 5: (5,1), (5,5), (5,4)

BEGIN
5 1 1
4 1 1
1 1 1
5 1 4
5 4 4
1 1 4
1 4 4
4 1 4
4 4 4
5 5 4
4 5 4
5 1 5
5 5 5
5 4 5
END