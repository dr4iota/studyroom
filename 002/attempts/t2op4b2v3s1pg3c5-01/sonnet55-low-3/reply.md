Writes to x take effect in the order B2 (3), B3 (2), B4 (1), so x passes through 0, 3, 2, 1.

**Constraints**
- B1 and B2 happen before P, and A2 ends after P. So A3 takes effect after P, and therefore after B2, and cannot return 0.
- A2 is only required to end after P. It can take effect before B2 (returning 0) or at any later point.
- A2 takes effect before A3, so A2's value can't come later in the sequence 0, 3, 2, 1 than A3's value.
- A4 writes A3's value, and B4 writes 1 as B's last write. The final value of x is therefore either 1 (B4 lands last) or A3's value (A4 lands last).

**Cases**
- A3 = 3: A2 can be 0 or 3, and the final value is 3 or 1.
- A3 = 2: A2 can be 0, 3 or 2, and the final value is 2 or 1.
- A3 = 1: A2 can be 0, 3, 2 or 1, and the final value is 1.

BEGIN
0 3 3
0 3 1
3 3 3
3 3 1
0 2 2
0 2 1
3 2 2
3 2 1
2 2 2
2 2 1
0 1 1
3 1 1
2 1 1
1 1 1
END