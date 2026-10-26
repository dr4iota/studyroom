**Answer:** the final value of y is always 3, and the final value of z is 2 or 3.

**1. What C2 forces.** C2 reads x = 2. The writes to x are A1 (1), A2 (3), B2 (5), B6 (the B4 value, 3), C5 (2) and A8 (the A7 value). C5 comes after C2 in thread C, so it cannot be the source. So A8 must write 2, which means A7 returned 2. A8 also takes effect before C2.

**2. What C7 forces.** C7 reads x = 3 after C5 has written 2. A8 already took effect before C2, so the only write of 3 that can come between C5 and C7 is B6. This gives the order C2 < C5 < B6 < C7.

**3. Final y.** The writes to y are A4 (3), A5 (2), B1 (3) and B7 (3). A5 is A's last write to y. B7 comes after B6, and B6 comes after C5, C2, A8 and A5 in that chain. So B7 is the last write to y, and the final y = 3.

**4. Final z.** C6 reads z = 3 after C4 wrote 4. B5 can supply that 3 by taking effect between C4 and C6. The last write to z is either B8 (3) or C8 (2). C8 comes after C7, and B8 comes after B7. Neither is ordered against the other, so either can be last. That gives a final z of 3 or 2.

**5. A schedule that works.** In order of taking effect:
- B1, B2, B3, C1
- B4 (reads 3, from C1)
- A1 through A8 (A3 reads 3 from C1; A6 and A7 read 2)
- C2 (reads 2 from A8), C3, C4
- B5 (writes 3 to z), C5
- C6 (reads 3 from B5)
- B6 (writes 3 to x)
- C7 (reads 3 from B6)
- B7
- then B8 and C8 in either order.

This agrees with every known result. Putting C8 last gives final z = 2, and putting B8 last gives final z = 3.

BEGIN
3 2
3 3
END