B9 is always 0 and the final z is always 0. The final x is 1 or 4, and the final y is 1 or 6, independently of each other.

**Ordering constraints.**
- B1 ends before P and A2 starts after P, so B1 takes effect before A2.
- B2 ends before Q and A8 starts after Q, so B2 takes effect before A8.
- A1 ends before S and B5 starts after S, so A1 takes effect before B5.
- A9 ends before R and B8 starts after R, so A9 takes effect before B8. Hence B8 and B9 come after every operation of thread A.

**Q1 and Q4 (B9 and final z).**
- Only A8 writes y, and B2 takes effect before A8, so B2 reads 0.
- B8 writes 0 to z. Nothing writes z after B8, because all of A is already done and the only other B write to z is B1. So B9 reads 0 and the final z is 0.

**Q3 (final y).**
- The only writes to z before A4 are A1 (6) and B1 (1), and both come before A4. Their order is free, so A4 reads 6 or 1.
- A6 writes A4's value to z. Nothing else writes z before A7, because B8 comes after A9. So A7 reads A4's value, and A8 writes it to y.
- Final y is therefore 1 or 6.

**Q2 (final x).**
- B7 writes 4 and A2 writes 1. A2 can come after B7. For example, A1, B1, B2, B3, B4, B5, B6, B7, A2, … is a valid order. A2 can also come earlier, which leaves 4 as the last write.
- Final x is therefore 1 or 4.

The choice for x (A2 versus B7) does not constrain the choice for y (A1 versus B1), so all four combinations occur.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
END