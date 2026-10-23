**Fixed orderings from the sync points**
- **Q:** A1–A3 happen before Q, and B2 onward happen after Q. So A3 < B2.
- **S:** A1 happens before S, and B3 onward happen after S. So A1 < B3.
- **R:** B1–B4 happen before R, and A4 onward happen after R. So B4 < A4.
- **P:** A1–A8 and B1–B6 happen before P. A9 and B7–B8 happen after P.

**A3 (needed for Q1).** The only writes to z are A1, A4, A5, A6, B4 and B8. A3 can only see A1, because A3 < B2 < B4 and all the other writes come later. So A3 returns 1.

**Q1: A7.** Thread A writes z in order: A4 = 1, A5 = 6, A6 = 1. B4 takes effect before R, so before A4. B8 takes effect after P, so after A7. So A7 sees A6's write and returns **1**.

**Q2: B6.** B3 writes 3 to x before B6 in thread B's order.
- A8 writes 1 to x. A8 is after R, which is after B4, and before P.
- B6 is after B5 and before P.
- So A8 can take effect either before or after B6.
- B6 returns **3** or **1**.

**Q3: final x.** The last writes to x are A9 (writes 1) and B7 (writes 5). Both come after P and can take effect in either order. Final x is **1** or **5**.

**Q4: final z.** B8 writes 3 after P. Every other write to z (A6 is A's last) takes effect before P. Final z is **3**.

The value of B6 is settled before P, and the final value of x is settled after P. So Q2 and Q3 can be combined freely.

BEGIN
1 3 1 3
1 3 5 3
1 1 1 3
1 1 5 3
END