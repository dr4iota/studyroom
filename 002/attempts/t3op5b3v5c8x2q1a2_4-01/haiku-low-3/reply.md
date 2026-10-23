The final value of z is whichever write to z takes effect last. The z-writes are A4 (3), B1 (4), B2 (2), B3 (5), and C2 (1).

- B1 and B2 are always followed by a later write in thread B (B2 and B3 respectively), so they can never be last.
- A4, B3, and C2 are each the final z-write in their own thread, and nothing constrains them relative to the other threads. Each can be scheduled last by running the other threads' operations earlier.

So the possible final values of z are 1, 3, and 5.

BEGIN
1
3
5
END