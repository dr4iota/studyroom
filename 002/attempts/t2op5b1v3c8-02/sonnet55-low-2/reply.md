Each outcome below is written as (B1, B3, final x).

**Setup.** A writes 3, then 1, then reads r, then writes r, then writes 2. B reads three times and finally writes the value its second read returned (b2). B's reads only see A's writes, since B4 comes after all of B's reads.

A's earlier writes put x through the values 0 → 3 → 1 → (r) → 2.

**Case 1: B4 takes effect before A5 (final is 2).**
- B1 and B3 see values from the sequence 0, 3, 1 in non-decreasing order. B cannot see 2 here, because B4 follows B3 and precedes A5.
- The pairs (B1, B3) are (0,0), (0,3), (0,1), (3,3), (3,1), (1,1).
- B4's write cannot change what B1 and B3 read, because A4's write comes after B's reads.

**Case 2: B4 takes effect after A5 (final is b2).**
- B4 comes after A3, so A3 reads 1 and A4 writes 1. The timeline is 0, 3, 1, 1, 2.
- Treat the values in time order 0 < 3 < 1 < 2. Then b1 ≤ b2 ≤ b3 in that order, and the final value equals b2.
- The final value can therefore be any value from b1 to b3 in that order, inclusive.

The pairs and finals from Case 2 are:
- b1=0, b3=0: final 0
- b1=0, b3=3: final 0 or 3
- b1=0, b3=1: final 0, 3 or 1
- b1=0, b3=2: final 0, 3, 1 or 2
- b1=3, b3=3: final 3
- b1=3, b3=1: final 3 or 1
- b1=3, b3=2: final 3, 1 or 2
- b1=1, b3=1: final 1
- b1=1, b3=2: final 1 or 2
- b1=2, b3=2: final 2

Case 1 adds only the finals of 2 for the six pairs listed above.

BEGIN
0 0 0
0 0 2
0 3 0
0 3 3
0 3 2
0 1 0
0 1 3
0 1 1
0 1 2
0 2 0
0 2 3
0 2 1
0 2 2
3 3 3
3 3 2
3 1 3
3 1 1
3 1 2
3 2 3
3 2 1
3 2 2
1 1 1
1 1 2
1 2 1
1 2 2
2 2 2
END