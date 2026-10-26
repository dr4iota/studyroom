Both final values of y are possible (0 and 4), and the final value of z is always 3.

**Step 1: what A1 read.** A2 writes the A1 value to z, and A3 then reads z and gets 0. Every write to z other than A2's puts a non-zero value there (2, 4, 5, 3, 3). So the last write to z before A3 must be A2, and it must have written 0. Therefore A1 read 0. This means A4 writes 0 to x, and A5 and A7 both write 0 to y.

**Step 2: what C5 read and C7 wrote.** C5 reads y = 4, and only B4 writes 4 to y. So B4 comes before C5, and C7 writes 4 to x.

**Step 3: where A4 sits relative to C7.** A8 reads x = 4. A4 writes 0 to x, so A4 cannot fall between C7 and A8. Since A4 comes before A8 in thread A, A4 must come before C7. A2 comes before A4, so A2 also comes before C7.

**Final value of y.** The writes to y are B4 (4), A5 (0) and A7 (0).
- **y = 4 is possible.** Run A1 through A7 early. Then run B4, C5, C7 and A8. B4 is the last write to y.
- **y = 0 is possible.** Run B4, then C5 (which reads 4), then A5, A6 and A7. A7 is the last write to y.

**Final value of z.**
- C1 and C2 come before C3 in thread C, and B1 comes before B5 in thread B. So none of them can be the last write to z.
- A2 cannot be the last write either. If A2 came after B5, it would have to fall between B5 and B8, because B8 comes after B7, which comes after C7, which comes after A2. Then B8 would read 0 instead of 3.
- So the last write to z is B5 or C3, and both write 3. The final value of z is always 3.

BEGIN
0 3
4 3
END