The final value of z can be 2 or 4.

**What B1 reads.** The only write to y is B3, and B3 comes after B1 in thread B. So B1 reads 0, and B2 and B3 both write 0.

**Writes to z.** There are four: A1 writes 2, B2 writes 0, C1 writes 1 and C2 writes 4.

**What B4 returning 4 requires.** The last write to z before B4 must be C2. B2 comes before B4 in thread B, so B2 must take effect before C2, otherwise z would be 0. C1 also comes before C2 in thread C. A1 must either take effect before C2 or after B4.

**Final value of z.** B2 and C1 always take effect before C2, so neither can be last. Only C2 or A1 can be the last write:
- If A1 takes effect before C2, the last write is C2, so z ends as 4.
- If A1 takes effect after B4, the last write is A1, so z ends as 2. This is consistent with A's other known results, because A2 still writes x=1 after A1 and A3 and A4 still read 1.

BEGIN
2
4
END