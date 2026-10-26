Every execution that fits the known results gives A6 = 1, and the final z is either 3 or 5.

**Where the z values come from**
- C8 returned 3. The z-writes are A1 (2), A2 (5), C6 (1) and B8 (the value B3 read). Only B8 can write 3, so B3 read 3 and B8 wrote 3.
- B8 must take effect after C6 and before C8, since B8 has to be the last write to z before C8.
- B4 returned 2. So A1 took effect before B4, and A2 had not yet taken effect. B8 comes after B4 in thread B anyway. This gives A1 < B4 < A2.

**Where the y values come from**
- A3 returned 2. Only C3 writes 2 to y before A4, so C2 and C3 both took effect before A3.
- A4 (write 1 to y) comes after A3. A8 comes after A6.
- So all of C's writes to y happen before A4, and the last write before A6 is A4. Q1 is therefore 1.

**Final z**
- A2 must come after B4. It can take effect before B8, or after C8, because otherwise C8 would read 5 instead of 3.
- If A2 comes before B8, B8 is the last write to z and the final z is 3.
- If A2 comes after C8, A2 is the last write and the final z is 5. A3 still reads 2 from y in this case, because C2 and C3 are done and A4 has not yet run.
- The x conditions can always be met. C7 comes after C5, so the last write to x is a 3 from either C7 or B5–B7.

BEGIN
1 3
1 5
END