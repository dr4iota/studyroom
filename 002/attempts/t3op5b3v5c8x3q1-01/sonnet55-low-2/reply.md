B3 can return 0, 1 or 5, but not 4.

**Writes to y.** The writes to y are A1 (writes 1), A5, B4 (writes 4) and C5.
- C2 reads x after C1 wrote 5. The only other write to x is C4, which comes after C2 in thread C, and B never writes x. So C2 returns 5, and C5 writes 5.
- A3 reads y after A1, so it returns 1, 4 (from B4) or 5 (from C5). A5 then writes that value.

**Possible values of B3:**
- **0:** B3 runs before any write to y.
- **1:** A1 takes effect before B3, with no later write before B3.
- **5:** C1, C2 and C5 all take effect before B3, with no later write to y before B3.
- **4 is impossible:** The only writes of 4 to y are B4 and A5 (when A3 read 4). B4 comes after B3 in thread B. A5 can write 4 only if A3 read 4, which needs B4 to have already taken effect, so A5 also comes after B3. No write of 4 can take effect before B3.

BEGIN
0
1
5
END