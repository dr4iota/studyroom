Writes to z come from three threads: A4 writes 3, B1–B3 write 4, 2, 5 in that order, and C2 writes 1. No constraints link the threads, so these writes can interleave in any order.

- **z = 3:** A4 takes effect after every other write to z.
- **z = 5:** B3 takes effect last. B3 is always B's final write to z, so it can come after A4 and C2.
- **z = 1:** C2 takes effect after A4 and after B3.
- **z = 4 or 2:** Not possible. B2 always follows B1, and B3 always follows B2. B's last write to z is therefore always 5.

So the final value of z can be 1, 3, or 5.

BEGIN
1
3
5
END