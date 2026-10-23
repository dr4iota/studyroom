Final value of z is the last write to z among: A4 (3), B1 (4), B2 (2), B3 (5), C2 (1).

No sync points or known results constrain the ordering, so the threads interleave freely. The last write is the final value of z.

Which writes can be last:
- B3 (5) is the last of B's z writes, but A4 and C2 can come after it, or before it. 5 is possible if B3 is last overall, with A4 and C2 earlier. Fine.
- A4 (3): put it last, after all of B's and C's writes. Possible.
- C2 (1): put it last. Possible.
- B1 (4) and B2 (2) are followed by B3 in thread B, so B3 lands after them. They can never be last.

So the possible final values are 3, 1, 5.

BEGIN
1
3
5
END