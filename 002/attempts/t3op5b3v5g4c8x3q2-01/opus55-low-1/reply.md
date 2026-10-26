The possible combinations are **(1, 1), (1, 0) and (0, 0)**. The combination (0, 1) is impossible.

**Step 1: A1 returns 0.** The only write to y is A2. A2 writes the value A1 read, and A2 comes after A1. So when A1 reads y, nothing has been written there yet, and it returns 0. B3's known result of 0 agrees with this.

**Step 2: A4 writes 0 to x.** A4 writes A1's value, so x only ever receives B1's write of 1 and A4's write of 0.

**Step 3: C4 comes after B1.** C2 returned 3, so a write of 3 to z (B2 or B4) took effect before C2. B2 comes after B1 in thread B, so B1 is before C2. C4 comes after C2 in thread C, so B1 is also before C4.

**Step 4: what C4 and the final x can be.**
- If A4 takes effect before B1, the last write to x is B1. C4 reads 1, and the final x is 1.
- If A4 takes effect after B1, the final x is 0. C4 reads 1 if A4 comes after C4, and 0 if A4 comes before C4.
- For C4 to read 0, A4 must come after B1 and before C4. Then A4 is also the last write to x, so the final x must be 0. That rules out (0, 1).

**Step 5: the z constraint can always be met.** Each case also needs C2 to see a 3, so both C1's 5 and A5's 2 must come before the 3-write that C2 reads, or after C2.
- Use the order C1, B1, B2, C2 for that part of the run.
- Place A5 after C2 in every case.

Example orders:
- (1, 1): A1, A2, A3, A4, C1, B1, B2, C2, C3, C4, A5, B3, B4
- (1, 0): A1, A2, C1, B1, B2, C2, C3, C4, A3, A4, A5, B3, B4
- (0, 0): A1, A2, C1, B1, B2, C2, A3, A4, C3, C4, A5, B3, B4

BEGIN
1 1
1 0
0 0
END