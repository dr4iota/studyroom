A2 can return 0 or 2, and never 4.

The only write to y is C4, which writes whatever C1 read from z. So A2 returns 0 if it reads before C4 takes effect, or else the value C1 read.

- **0:** A2 reads y before C4 takes effect, so it sees the initial 0.
- **2:** B1 writes 2 to z, C1 reads z and gets 2, C4 writes 2 to y, and then A2 reads y and gets 2. Nothing in the rules forbids this ordering.
- **4:** C1 would have to read 4 from z. The only writes of 4 to z are A4 and C5. C5 comes after C4 in thread C, so it cannot be the source. A4 comes after A2 in thread A, so C1's read of 4 (and then C4's write) would have to follow A2. A2 would therefore read y before C4 writes, and it cannot see 4.
- **Values A5 could write:** A5 also comes after A2, so it cannot contribute either.

BEGIN
0
2
END