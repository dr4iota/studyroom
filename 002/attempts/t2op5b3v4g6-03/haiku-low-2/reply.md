Each thread's operations keep their listed order, and the known reads add constraints:

- B1 reads 0, so B1 takes effect before A5, B2, B3, and B4, since each of those writes a nonzero value to x.
- B5 reads 4 from z, so A3 (write 4 to z) takes effect before B5.
- A2 reads 0 from z, which program order already guarantees, since A2 comes before A3.

I encoded each interleaving by how many A-operations precede each B-operation, then derived the three asked values:

- **A1** returns the latest of B2, B3, B4 that takes effect before it (0 if none).
- **A4** returns the latest of B2, B3, B4 that takes effect before it (A5 comes after A4 in program order).
- **Final x** is 2 if B4 comes after A5, and 3 otherwise.

Enumerating the valid interleavings gives these 14 distinct outcomes:

BEGIN
0 0 2
0 0 3
0 1 2
0 1 3
0 2 2
0 2 3
1 1 2
1 1 3
1 2 3
2 1 2
2 1 3
2 2 2
2 2 3
END