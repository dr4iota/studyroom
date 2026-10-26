Q3 is always 4, and Q1 and Q2 each vary independently between 0 and 4.

- **Q3 (A7's read of y):** B4 reads y before B5, and B5 reads x. B3 (which writes 4 to x) is before B5 in B's program order. The only other writes to x (A4 and A6) come after P, which is after B6, so B5 always reads 4. B8 then writes 4 to y, and B8 precedes Q, which precedes A7. B2 writes 2 to y earlier, but B8 is later, so A7 reads 4.
- **Q2 (A3's read of x):** The only write to x that can precede A3 is B3 (value 4). A3 ends before R, and A4 comes after A3, so A3 reads 4 if B3 took effect before A3, and 0 otherwise. Both orders are feasible.
- **Q1 (A2's read of z):** Writes to z that can precede A2 are B1 (value 4) and B6 (value 4, since B5 reads 4). B9 (value 3) is after B7, which is after R, which is after A3 and therefore after A2, so it cannot precede A2. A5 (value 2) comes after A4 and cannot precede A2 either. So A2 reads 4 if B1 took effect before A2, and 0 otherwise. Both orders are feasible.

Each combination of Q1 and Q2 is realizable. For example, `B1 A1 A2 A3 R B2 B3 B4 S B5 B6 P A4 ... ` gives (4, 0, 4), and `A1 A2 B1 B2 B3 A3 R B4 S B5 B6 P A4 ...` gives (0, 4, 4).

Values in the order Q1 Q2 Q3:

BEGIN
0 0 4
0 4 4
4 0 4
4 4 4
END