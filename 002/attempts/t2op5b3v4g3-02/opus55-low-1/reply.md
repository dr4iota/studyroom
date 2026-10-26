Every combination of the three asked values is possible, giving 12 outcomes.

**Which values each question can take**
- **Q1 (A1 reads y):** Only B2 writes y, and it writes 4. So A1 returns 0 if it takes effect before B2, or 4 if after. B1 returning 0 only requires B1 to come before B2, which B's own order already guarantees.
- **Q2 (B3 reads x):** B3 comes before B5 in thread B, so it can only see A's writes or the initial 0.
  - It returns 0 if it takes effect before A2.
  - It returns 2 if it is between A2 and A3, or after A5.
  - It returns 4 if it is between A3 and A5.
- **Q3 (final x):** The last write to x is either A5 (value 2) or B5 (value 4).

**Why every combination can happen**
- **A1 returns 4:** Order B1, B2, A1 first. B3 can still fall before A2, between A2 and A3, or between A3 and A5. In each of those positions, B5 can take effect before or after A5. So B3 can be 0, 2 or 4, each with a final x of 2 or 4.
- **A1 returns 0:** A1 simply goes first. B's operations can then be placed in all the same ways as above.
- **B3 returns 2 by reading A5:** In that case B5 comes after A5, so the final x is 4. This adds no new combination, because B3 = 2 with a final x of 4 is already reachable by placing B3 between A2 and A3.

Every value of Q1 (2 choices) combines with every value of Q2 (3 choices) and Q3 (2 choices).

BEGIN
0 0 2
0 0 4
0 2 2
0 2 4
0 4 2
0 4 4
4 0 2
4 0 4
4 2 2
4 2 4
4 4 2
4 4 4
END