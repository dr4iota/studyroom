For any execution, the reads of x by A2 and A4 depend on where they fall among B's writes, and B1 depends on whether A's write comes before it.

**Case B1 = 1.** B1 runs before B2, so the only write that can precede it is A5. If A5 takes effect before B1, then A1–A4 all come before A5. They therefore also come before every write by B. So A2 = 0 and A4 = 0, which gives the combination 0 0 1.

**Case B1 = 0.** Then no write precedes B1. A5 comes after A4, so A5 cannot affect A2 or A4. Those two reads therefore see the values of x as B moves through its writes: 0, 1, 2, 3, 1 (positions 0 to 4). A2 sees the value at some position i, and A4 at a position j with i ≤ j. Any such pair is achievable.

- i = 0 (value 0): A4 can be 0, 1, 2, 3 or 1.
- i = 1 (value 1): A4 can be 1, 2, 3 or 1.
- i = 2 (value 2): A4 can be 2, 3 or 1.
- i = 3 (value 3): A4 can be 3 or 1.
- i = 4 (value 1): A4 is 1.

Removing duplicates, the (A2, A4) pairs are: 00, 01, 02, 03, 11, 12, 13, 21, 22, 23, 31, 33.

BEGIN
0 0 0
0 1 0
0 2 0
0 3 0
1 1 0
1 2 0
1 3 0
2 1 0
2 2 0
2 3 0
3 1 0
3 3 0
0 0 1
END