Each read of x by B1 and B2 can only see values written by A1 and A2, because B's own writes come after both reads. So B1 ≤ B2 in time order, and the x values they see follow the sequence 0, 3, 1. The possible (B1, B2) pairs are (0,0), (0,1), (0,3), (3,3), (3,1) and (1,1).

The final y equals A3's result. A3 runs after A2 has written 1, so it reads either 1 or a value written by B3 or B4 after A2. B3 writes B1's value and B4 writes B2's value.

- **(0,0):** B writes only 0, so y is 0 or 1.
- **(0,1):** B3 writes 0 and B4 writes 1, so y is 0 or 1.
- **(0,3):** B3 writes 0 and B4 writes 3. A3 can read 1, 0 or 3, so y is 0, 1 or 3.
- **(3,3):** B writes only 3, so y is 1 or 3.
- **(3,1):** B3 can write 3 after A2, so y is 1 or 3.
- **(1,1):** B writes only 1, so y is 1.

BEGIN
0 0 0
0 0 1
0 1 0
0 1 1
0 3 0
0 3 1
0 3 3
3 3 1
3 3 3
3 1 1
3 1 3
1 1 1
END