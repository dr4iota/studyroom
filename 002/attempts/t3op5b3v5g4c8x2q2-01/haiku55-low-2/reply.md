Q1 is always 0, and Q2 can be 0, 1, or 5.

**Q1 (C3's value) is always 0.** Only B5 writes z, and it writes B4's value. C4 returns 0, so either B5 has not taken effect before C4, or B5 wrote 0. If B5 took effect before C4 with a nonzero value, C4 would return that value. So any write to z that C3 could see is either absent or 0.

**Q2 (final z) equals B4's value.** B5 is the only write to z and always takes effect, so the final z is the value B5 wrote. B4 reads y. The writes to y are B1 (2), B3 (1), C1 (1), and A4 (the value A1 read, which is 0 or 5). B3 always precedes B4, so B4 reads 1 (from B3 or C1) or A1's value (from A4). That gives possible values 0, 1, and 5.

Each value is achievable:
- **5:** B2 before A1, so A1 reads 5. A4 writes 5 to y after B3, and B4 reads 5. B5 runs after C4, which keeps C4 at 0.
- **1:** B4 reads B3's write of 1. B5 runs after C4.
- **0:** A1 reads 0 (before B2). A4 writes 0 to y after B3, and B4 reads 0. B5 writes 0 to z, which keeps C4 at 0.

BEGIN
0 0
0 1
0 5
END