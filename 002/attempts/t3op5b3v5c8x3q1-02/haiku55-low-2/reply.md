Only C4 writes to y, and it writes the value C1 read from z. So A2 can return 0 (its initial value) or whatever C1 read.

- **0:** A2 takes effect before C4 writes y. Possible.
- **2:** B1 writes 2 to z, C1 reads 2 before any later write to z, C4 writes 2 to y, and then A2 reads 2. Possible, since no sync points constrain the threads.
- **4:** A4 (which writes 4 to z) comes after A2 in thread A, so A2 takes effect before A4. C1 can only read 4 after A4, and C4 can only write y after C1. So A2 always takes effect before any write of 4 to y. Impossible.

Q1 (the value returned by A2) can be 0 or 2.

BEGIN
0
2
END