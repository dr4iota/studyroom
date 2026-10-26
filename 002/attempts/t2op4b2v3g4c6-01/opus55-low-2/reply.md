**Approach**

Nothing writes y, so A1 always returns 0. A2, A3 and A4 then run in order.

Thread B writes x in a fixed order: 3, then 2, then 1. So x goes through the values 0 → 3 → 2 → 1, apart from A4's own write.

B1 must return 0, so it takes effect before B2. The only way x could be non-zero then is if A4 had already written a non-zero value. A4 writes what A3 read. If A4 came before B1, A3 also came before any write by B, so A3 read 0 and A4 wrote 0. So B1 = 0 holds in every case.

**A2 and A3**

A4 takes effect after A2 and A3, so neither of those reads can see A4's write. Each sees one point in B's sequence 0, 3, 2, 1. A3 takes effect after A2, so A3 sees the same point or a later one.

That gives these (A2, A3) pairs:
(0,0), (0,3), (0,2), (0,1), (3,3), (3,2), (3,1), (2,2), (2,1), (1,1).

**Final x**

A4 writes v, the value A3 read.
- If A4 takes effect after B4, the final value is v.
- If A3 took effect before B4 (v is 0, 3 or 2), A4 can instead come before B4. Then B4 overwrites it and the final value is 1.
- If v = 1, the final value is 1 either way.

So:
- A3 = 0 → final 0 or 1
- A3 = 3 → final 3 or 1
- A3 = 2 → final 2 or 1
- A3 = 1 → final 1

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