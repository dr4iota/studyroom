Both final values 3 for y, and 2 or 3 for z, are possible. The reasoning follows.

**Fixing the order of the key operations**

- C2 read x = 2. The only write of 2 to x that can precede C2 is A8, which copies A7's value. (B6 writes 3, and C5 comes after C2.) So A7 read 2, which means A5 came before A7, and A8 took effect before C2.
- C7 read x = 3. A2 is overwritten by A8, because A2 comes before A8 in thread A. So the 3 must come from B6, which copies B4's value of 3. B6 therefore takes effect after C2 and before C7. C5, which writes 2 to x, must fall either before B6 or after C7.

**Q1: final y**

The writes to y are A4, A5, B1 and B7. B7 comes after B6, which comes after A8, which comes after A7, which comes after A5. A4 and B1 also come before B7. So B7 is the last write, and y = 3 in every valid execution.

**Q2: final z**

B8 comes after B6. C8 comes after C7. Every other write to z comes before one of these two, so the last write is either B8 (value 3) or C8 (value 2).

- **z = 3:** B8 takes effect after C8.
- **z = 2:** C8 takes effect after B8.

Both are consistent with the known reads:

- A3 and B4 can read 3 from C1.
- C6 can read 3 from B5, which writes after C4.

**Result**

BEGIN
3 2
3 3
END