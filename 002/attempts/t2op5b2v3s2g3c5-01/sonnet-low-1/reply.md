Final y is always 1. Here is why, and then how A1 and B3 can combine.

**Final value of y.** B's steps through B4 come before Q. A5 starts after Q and ends at P. B5's write takes effect after P. So B5's write of 1 is the last write to y, after A1–A4 (all before A5) and B1–B4.

**Interleaving.** A1–A4 and B1–B4 can interleave freely, since B1–B4 are before Q and A1–A4 may fall on either side of Q. Let a be the value A1 reads and b the value B3 reads.

**What A1 can read.** A1 comes before A2 and A4, so it can only see the initial 0, B1's 1, B2's 3, or B4's write. B4 writes b, which comes from B3.
- A1 cannot read 2. Only A4 writes 2, and A4 comes after A1. B4 could write 2 only if B3 had read A4's 2, which would put A4 before A1.
- So a is 0, 1 or 3.

**What B3 can read.** B1 and B2 come before B3, so B3 sees the last write to y before it. That is 3 from B2, or a from A2, or 2 from A4.

**Pairs (a, b).**
- a=0: A1 reads before B1. B3 can read 3, 0 (A2 after B2) or 2 (A4). This gives (0,0), (0,2), (0,3).
- a=1: A1 reads between B1 and B2. B3 can read 3, 1 (A2 after B2) or 2. This gives (1,1), (1,2), (1,3).
- a=3: A1 reads after B2. B3 can read 3 or 2. This gives (3,2) and (3,3). B3 cannot read 0 or 1, because B2's 3 has overwritten them and A2 writes 3.

BEGIN
0 0 1
0 2 1
0 3 1
1 1 1
1 2 1
1 3 1
3 2 1
3 3 1
END