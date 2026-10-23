Only the value y holds when A2 takes effect matters, and only C4 writes y. C4 writes the value C1 read from z, and z can hold 0, 2, or 4 when C1 reads it:

- **0:** C1 runs before any write to z, then C4 writes 0 to y. A2 can read y before C4, giving 0.
- **2:** B1 writes 2 to z, C1 reads 2, C4 writes 2 to y, and A2 reads y after that, giving 2.
- **4:** A4 writes 4 to z, C1 reads 4, C4 writes 4 to y, and A2 reads y after that, giving 4. A4 precedes A2 within thread A, so this order is valid.

Thread A has no sync points tying it to the other threads, so A2 can take effect at any point relative to the others. Each of the three values is therefore reachable.

BEGIN
0
2
4
END