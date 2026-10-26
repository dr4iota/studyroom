Each read of x returns whatever x holds at that moment. A4 writes back what A3 read. The y read (A1 returned 0) is consistent with every execution, since nothing writes y.

**Order of values in x from thread B.** B1 reads 0, so B1 takes effect before B2. Even if A4 took effect earlier, it would write 0 when A3 read 0, so this still holds. Thread B then writes 3, 2, 1 in that order. Before A4 takes effect, x therefore steps through 0 → 3 → 2 → 1.

**A2 and A3.** A2 takes effect before A3, and A4 cannot take effect until after A3. So both reads see values from the sequence 0, 3, 2, 1. A3 must see the same value as A2 or one later in that sequence. That gives 10 pairs:
(0,0), (0,3), (0,2), (0,1), (3,3), (3,2), (3,1), (2,2), (2,1), (1,1).

**Final value of x.** Call A3's value b.
- A4 can always take effect after B4. Then the final value is b.
- If b is not 1, A3 took effect before B4. A4 can then also take effect before B4, which makes the final value 1.
- If b is 1, A3 took effect after B4, so A4 does too, and the final value is 1 either way.

So each pair gives final value b, plus final value 1 when b is not 1.

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