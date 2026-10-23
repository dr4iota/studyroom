**Q2 (value returned by B2) must be 0.**
- Suppose B2 returned some v ≠ 0. That value can only come from A3, so A3 took effect before B2.
- Then B3 writes v to x, and B4 runs after B3.
- B4 is known to return 0. That needs a write of 0 to x after B3.
- The only other write to x is A3, and it is already before B2. So no such write exists, and B2 must return 0.
- This fits every other known result. B2 reads 0, B3 writes 0, and B4 and C4 read 0. Neither B4 nor C4 needs to be ordered against A3 in a way that breaks this.

**Q1 (value returned by A4) can be 0, 5 or 1.**
- The writes to z are B1 (5), C2 (5) and C3 (1).
- A4 reads 0 if it takes effect before all of them.
- It reads 5 if it follows B1 or C2 but not C3, or follows C3 and then B1.
- It reads 1 if C3 is the last write to z before A4.

**Q3 (final value of y) can be 3 or 4.**
- The writes to y are A5 (3) and C1 (4). Whichever takes effect last decides.

**How Q1 and Q3 interact:**
- The final y is 4 only if C1 comes after A5. Then C1 is after A4, since A4 runs before A5 in thread A.
- Since C2 and C3 come after C1, C3 is then also after A4. So A4 cannot read 1 in that case. It can still read 0, or 5 from B1.
- A final y of 3 works with every value of A4.

BEGIN
0 0 3
0 0 4
5 0 3
5 0 4
1 0 3
END