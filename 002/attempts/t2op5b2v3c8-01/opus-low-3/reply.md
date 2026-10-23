The final value of y is whatever A3 read, since A4 writes it. So the task is to find, for each possible pair of values read by B1 and B2, which values A3 can read.

**Values B1 and B2 can read.** Both reads happen before B's own writes (B3 and B4 come after B2). So they can only see writes made by thread A. Over time, x holds 0, then 3 (after A1), then 1 (after A2). B2 runs after B1, so it sees the same value or a later one. That gives six possible pairs:

- (0,0), (0,3), (0,1)
- (3,3), (3,1)
- (1,1)

**Values A3 can read.** A3 runs after A2, so it reads one of three writes:

- **A2's 1:** A3 runs right after A2, before B3 takes effect. This works for every pair.
- **B3's value (what B1 read):** B3 takes effect between A2 and A3, and B4 takes effect after A3. A2 can always be placed before B3 without changing what B1 and B2 read, so this works for every pair.
- **B4's value (what B2 read):** B4 takes effect between A2 and A3. The same reasoning applies, so this also works for every pair.

So for each pair, y can be 1, the value B1 read, or the value B2 read.

**Combining these:**

| B1 | B2 | Possible y |
|----|----|------------|
| 0 | 0 | 0, 1 |
| 0 | 3 | 0, 1, 3 |
| 0 | 1 | 0, 1 |
| 3 | 3 | 1, 3 |
| 3 | 1 | 1, 3 |
| 1 | 1 | 1 |

BEGIN
0 0 0
0 0 1
0 3 0
0 3 1
0 3 3
0 1 0
0 1 1
3 3 1
3 3 3
3 1 1
3 1 3
1 1 1
END