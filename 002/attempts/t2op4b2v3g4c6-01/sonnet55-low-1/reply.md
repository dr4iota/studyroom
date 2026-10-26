Thread A only reads y, and nothing writes y, so A1 returns 0 trivially. B1 reads before B2 takes effect, so it always returns 0 and adds no constraint.

**Order of values in x.** B's writes take effect in the order 3, 2, 1. Until A4 takes effect, the values of x over time are therefore 0, 3, 2, 1 in that order. A2 and A3 both take effect before A4, and A2 takes effect before A3. So A2 reads a value no later in that sequence than the value A3 reads.

**Possible (A2, A3) pairs:**
- A2 = 0: A3 can be 0, 3, 2 or 1.
- A2 = 3: A3 can be 3, 2 or 1.
- A2 = 2: A3 can be 2 or 1.
- A2 = 1: A3 must be 1.

**Final value of x.** A4 writes A3's value. The final value depends on whether B4 or A4 takes effect last.
- If B4 is last, the final value is 1. This is always possible. A4 can take effect before B4 when A3 read 0, 3 or 2, and A4 is necessarily after B4 when A3 read 1.
- If A4 is last, the final value is A3's value. A4 can be delayed until after B4 for any A3 value.

So for each A3 value, the possible final values are:
- A3 = 0: final 0 or 1.
- A3 = 3: final 3 or 1.
- A3 = 2: final 2 or 1.
- A3 = 1: final 1 only.

BEGIN
0 0 0
0 0 1
0 3 1
0 3 3
0 2 1
0 2 2
0 1 1
3 3 1
3 3 3
3 2 1
3 2 2
3 1 1
2 2 1
2 2 2
2 1 1
1 1 1
END