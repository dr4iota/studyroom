The possible outcomes are six combinations of (Q1, Q2, Q3, Q4), listed below.

Key findings:
- **A3 always reads 1.** Only A1 can have written z before A3, since every other z write is ordered after A3.
- **A7 reads 1 or 3.** It reads 3 only if B8 lands between A6 and A7. Otherwise it reads 1.
- **B6 reads 1 or 3.** The write of 3 by B3 always precedes B6. The write of 1 comes from A8 (which writes A7's value), and only if A8 precedes B6. B6 can read 1 only when A7 read 1 and A8 precedes B6.
- **Final x is 1 or 5.** A9 always writes 1 and follows A8 and P. B7 writes 5 and can land after A9 or before it.
- **Final z is 1 or 3.** B8 writes 3, and it lands either before or after A6's write of 1.

Consistent combinations:
- Q1=1, Q2=1: A8 precedes B6, which forces B8 after A7, so final z is 3. Final x can be 1 or 5.
- Q1=1, Q2=3: B8 can land before A6 (final z = 1, and then B7 must precede A9, so final x = 1), or after A7 (final z = 3, with final x either 1 or 5).
- Q1=3, Q2=3: B8 lands between A6 and A7, which forces B7 before A9, so final x = 1 and final z = 3.
- Q1=3, Q2=1 is impossible, because B6 can only see A8's value of 1 if A7 read 1.

BEGIN
1 1 1 3
1 1 5 3
1 3 1 1
1 3 1 3
1 3 5 3
3 3 1 3
END