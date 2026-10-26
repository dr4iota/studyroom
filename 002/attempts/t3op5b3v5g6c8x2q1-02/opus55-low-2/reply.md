**Possible final values of y: 2 and 5.**

1. **What B3 reads.** The only write to z is A1, which writes 5. B2 has already read 5, so B3 comes after A1 and also reads 5. Therefore B4 writes 5 to y and B5 writes 5 to x.

2. **The writes to y.** There are four: C1 writes 1, C4 writes 4, A4 writes 2 and B4 writes 5.

3. **Limits from the known reads.**
   - A2 returned 1, so A2 comes after C1, and no other write to y takes effect between C1 and A2.
   - A3 returned 4, so A3 comes after C4, and neither A4 nor B4 takes effect between C4 and A3.
   - A4 comes after A3 in thread A, so A4 is after C4.

4. **Which write can be last.** C4 is before A4, so C4 cannot be last. C1 is before C4 in thread C, so it cannot be last either. The final value of y is therefore set by A4 (2) or B4 (5), whichever takes effect later.

5. **Final y = 5 is possible.** Let B4 come after A4. For example: A1, C1, A2, B1, C2, C3, C4, A3, A4, B2, B3, B4, B5.
   - A2 reads 1 and A3 reads 4.
   - B2 and C2 each read z = 5.
   - C3 reads x = 1, because B1 came before it and B5 has not happened yet.

6. **Final y = 2 is possible.** Let B4 come between A2 and C4. For example: A1, C1, A2, B1, B2, B3, C2, C3, B4, C4, A3, A4, B5.
   - A2 reads 1, since B4 has not yet happened.
   - A3 reads 4, since B4 was overwritten by C4.
   - C3 reads x = 1, because B5 comes later.
   - A4 is the last write to y.

BEGIN
2
5
END