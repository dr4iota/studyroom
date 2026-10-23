Q1 can only be 0.

A2 reads y, and A3 then writes that value to z. A5 later reads z and must return 0.

Every other write to z is nonzero:
- B1 writes 4 to z.
- C5 writes the value C3 read from y. C3 comes after C2, which writes 1 to y, and y is only ever written with 1 or 5, so C3 never reads 0.

A3 always runs before A5, so the last write to z before A5 is either A3 or a later write by B1 or C5. If A2 returned 1 or 5, A3 would write a nonzero value and z could not read 0 at A5. So A2 must be 0.

This is achievable with the order A1, B1, A2 (reads 0), A3 (writes 0 to z), C1, C2, A4 (reads 1), A5 (reads 0), and then the remaining operations. C5 comes after A5, so it does not disturb z.

BEGIN
0
END