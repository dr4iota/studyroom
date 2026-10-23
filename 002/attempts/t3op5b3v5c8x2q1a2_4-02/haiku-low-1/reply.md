A2 can return **0** or **4**.

- **0:** A2 runs before any write to x takes effect.
- **4:** C1 writes 4 to y, C4 reads 4, C5 writes 4 to x, and then A2 reads x before anything overwrites it.

The other values cannot occur:

- The only writes to x are A4 and C5. A4 comes after A2 in thread A, so it never affects A2.
- C5 writes the value C4 read from y. The only nonzero value that can ever enter y is 4 (from C1). Otherwise y receives B4's value, which is a copy of some earlier value of x.
- So before A2, every nonzero value in x or y must trace back to 4 from C1. Values 1 and 2 can only enter the system through A4, which is after A2.

BEGIN
0
4
END