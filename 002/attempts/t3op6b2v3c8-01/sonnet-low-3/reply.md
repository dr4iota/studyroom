All twelve combinations are possible. Every write to x stores either 2 (from B1 or C1) or a value read from x, so x only ever holds 0 or 2.

**Possible values**
- A4 can be 0 (read before any write to x) or 2 (read after B1 or C1).
- B2 can be 0 only if A3 read 0, and A5 then wrote that 0 to x after B1 and before B2. Otherwise B2 is 2.
- y can be written with B2's value (0 or 2) by B3, and with 1 by C2. B5 therefore can return 0, 1 or 2.
- The final x is 0 if the last write to x is a 0 written by A5 or B4. Otherwise it is 2.

**Constructing each case**

*B5 = 0* needs B3 to write 0 to y (so B2 = 0) and C2 to come after B5. One schedule:
1. A1–A3 read 0.
2. B1 writes 2.
3. A4 reads 2 (or reads 0 if it ran before B1).
4. A5 writes 0.
5. B2 reads 0, then B3 writes 0 to y.
6. For final x = 0: C1 writes 2, then B4 writes 0, then B5 reads 0, then C2 runs. For final x = 2: B4 writes 0, then C1 writes 2, then B5 reads 0, then C2 runs.

*B5 = 1* has C2 write 1 to y after B3 and before B5.

*B5 = 2* has B2 = 2, so B3 writes 2 to y, and C2 runs after B5.

Each of these works with A4 = 0 or 2. Final x = 0 comes from A5 writing 0 last, which needs A3 = 0, so A3 runs before B1 and C1. Final x = 2 comes from C1 or B1 writing last.

BEGIN
0 0 0
0 0 2
0 1 0
0 1 2
0 2 0
0 2 2
2 0 0
2 0 2
2 1 0
2 1 2
2 2 0
2 2 2
END