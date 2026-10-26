Every execution has to be ordered so that each operation takes effect at a single instant. Here is the reasoning.

**Constraints**
- Nothing ever writes to y, so A1 returning 0 is always consistent.
- B1 must read x before any write to x takes effect. In particular it comes before A4, so it returning 0 is always possible.
- B's writes take effect in order: 3, then 2, then 1. So before A4 takes effect, x moves through 0, 3, 2, 1.
- A2 and A3 both take effect before A4. A3 comes after A2, so A3 reads the same state of x as A2 or a later one in the sequence 0, 3, 2, 1.

**Final value of x**
- If A4 takes effect after B4, x ends at 2.
- If A4 takes effect before B4, x ends at 1.
- If A3 read 1, then B4 has already taken effect before A4, so x must end at 2.
- Otherwise A4 can fall either before or after B4, so x can end at 1 or at 2.

**Possible (A2, A3) pairs**
- A2 = 0: A3 can be 0, 3, 2 or 1.
- A2 = 3: A3 can be 3, 2 or 1.
- A2 = 2: A3 can be 2 or 1.
- A2 = 1: A3 must be 1.

BEGIN
0 0 1
0 0 2
0 3 1
0 3 2
0 2 1
0 2 2
0 1 2
3 3 1
3 3 2
3 2 1
3 2 2
3 1 2
2 2 1
2 2 2
2 1 2
1 1 2
END