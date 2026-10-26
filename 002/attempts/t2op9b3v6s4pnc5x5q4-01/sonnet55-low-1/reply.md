Reasoning from the sync constraints, with x, y, z all starting at 0:

- B1–B8 all end before P and Q. A1 starts after Q, so it starts after B8. B9 is unconstrained except that it follows B8.
- A writes y only at A4, which comes after A1. So B2 reads 0, and B8 writes 0 to y. B4's 3 is overwritten, and A1 reads 0.
- B5 reads 4, because only B1 and B3 write x before it and B3 is the last. B9 writes the value B2 read, which is 0, so x is 0 once B9 happens.
- x is 4 from B3 until B9 and 0 after B9. A never writes x, so A's reads of x are 4 up to B9 and 0 afterward.

Cases:
- **B9 after A3:** A3 reads 4, so A4 writes 4 to y and the final y is 4. A5, A6 and A8 read in order and can switch from 4 to 0 once, giving 444, 440, 400 or 000.
- **B9 before A3:** A3 reads 0, so A4 writes 0 and the final y is 0. A5, A6 and A8 all read 0.

BEGIN
4 4 4 4
4 4 0 4
4 0 0 4
0 0 0 4
0 0 0 0
END