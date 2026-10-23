Only two final values of z are possible: 4 and 2.

- **B1 must read 0.** The only write to y is B3, which comes after B1 in thread B's order. So B2 writes 0 to z, and B3 writes 0 to y. C3 also reads 0 from y.
- **B4 = 4 constrains the z writes.** The last write to z before B4 must be C2 (value 4). So C2 takes effect before B4, and neither A1 nor B2 can take effect between C2 and B4. Because B2 comes before B4 in its thread, B2 must come before C2.
- **Final z is 4 if C2 is last.** This happens when A1 takes effect before C2. For example, A1, B1, B2, C1, C2, B3, B4 gives final z = 4.
- **Final z is 2 if A1 is last.** A1 can take effect after B4, since nothing forces it earlier. For example, B1, B2, C1, C2, B3, B4, A1, A2, A3, A4 gives final z = 2.
- **0 and 1 are impossible.** B2 and C1 both take effect before C2, so neither can be the last write to z.

BEGIN
2
4
END