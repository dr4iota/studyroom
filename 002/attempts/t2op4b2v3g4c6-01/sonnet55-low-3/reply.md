Block y is never written, so A1 always returns 0 and does not affect anything else. Only x matters.

**Writes to x.** B2, B3 and B4 take effect in that order, so x goes 0, 3, 2, 1. The only other write is A4, which writes A3's value and takes effect after A3.

**Reads.** B1 reads 0, so it takes effect before B2, which is always possible. A2 and A3 run in order, so each returns a value from the sequence 0, 3, 2, 1, and A3's value is at or later than A2's. A4's write cannot change what A2 or A3 return, because it happens after both.

**Possible (A2, A3) pairs:**
- A2 = 0: A3 can be 0, 3, 2 or 1.
- A2 = 3: A3 can be 3, 2 or 1.
- A2 = 2: A3 can be 2 or 1.
- A2 = 1: A3 can only be 1.

**Final value of x.** B4 is the last B write, so the final value depends on whether A4 lands before or after B4.
- If A4 takes effect before B4, B4 overwrites it and the final value is 1. This is possible whenever A3 read a value before B4 took effect, so any A3 value other than 1.
- If A4 takes effect after B4, the final value is A3's value.

This gives the following finals for each A3 value:
- A3 = 0: final is 0 or 1.
- A3 = 3: final is 3 or 1.
- A3 = 2: final is 2 or 1.
- A3 = 1: final is 1.

BEGIN
0 0 0
0 0 1
0 3 3
0 3 1
0 2 2
0 2 1
0 1 1
3 3 3
3 3 1
3 2 2
3 2 1
3 1 1
2 2 2
2 2 1
2 1 1
1 1 1
END