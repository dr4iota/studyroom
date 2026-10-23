A2 can only return 0 or 4.

A4 runs after A2 in thread A, so A4's write can never be what A2 reads. The only other writer of x is C5, which writes whatever C4 read from y.

C4 can read y as 0, 4 (from C1), or a value B4 wrote. B4 writes whatever B3 read from x. B3 can read x as 0, C5's value, or A4's value.

- **Value 0:** A2 runs before C5 takes effect, so it reads the initial 0.
- **Value 4:** C1 writes 4 to y, C4 reads 4, C5 writes 4 to x, and A2 reads x afterward. This is consistent.
- **Values derived from A4:** this would need B3 to read A4's write, then B4 to write y, then C4 to read it, then C5 to write x, and finally A2 to read it. That puts A4 before A2, but A4 is after A2 in thread A, which is a cycle, so it is impossible.
- **Values derived from C5 itself:** this would need C5's write to feed B3, then B4, then C4, then C5, which is circular, so it is impossible.

Any other value, such as 1 or 2, would have to come through one of these two routes, so only 0 and 4 remain.

BEGIN
0
4
END