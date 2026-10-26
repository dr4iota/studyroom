The possible outcomes are these six combinations of (Q1 a7, Q2 b6, Q3 final x, Q4 final z):

- **A3 always reads 1.** B4 and B8 both take effect after Q, which is after A3, so only A1 can be the last write to z before A3.
- **A7 is 1 or 3.** The last z write before A7 is A6 (value 1), unless B8 falls between A6 and A7 (value 3).
- **B6 is 3 or a7.** B3 always writes 3 to x before B6. A8 (value a7) is seen only if it takes effect before B6.
- **Final x is 1 or 5.** A8 always precedes A9, which writes 1, and B3 is never last. So the last x write is A9 (1) or B7 (5).
- **Final z is 1 or 3.** Only A6 (1) or B8 (3) can be last.

Checking which combinations of these are jointly achievable gives:

- a7=1, b6=1: final z is forced to 3, and final x can be 1 or 5.
- a7=1, b6=3: final x=1 with final z=1 or 3, or final x=5 with final z=3.
- a7=3, b6=3: B8 falls between A6 and A7, which forces B7 before A9, so final x=1 and final z=3.

BEGIN
1 1 1 3
1 1 5 3
1 3 1 1
1 3 1 3
1 3 5 3
3 3 1 3
END