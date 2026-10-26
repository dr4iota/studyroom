Both outcomes are possible: y ends as 0 or 4, and z always ends as 3.

**Step 1: A1 must read 0.** A2 writes A1's value to z, and A3 then reads z = 0. Every other write to z puts a non-zero value there, so the last write before A3 must be A2. That means A1 read 0. So A2, A4, A5 and A7 all write 0. Also, A1 must take effect before C4, the first non-zero write to x.

**Step 2: Final z is 3.** B8 reads z = 3, and B8 comes after B7. B7 reads x = 4, and only C7 writes 4 to x, so B7 is after C7. A8 reads x = 4 and comes after A4, so C7 is after A4, which is after A2. So B8 takes effect after A2. For B8 to see 3, some write of 3 (B5 or C3) must take effect after A2. Only B5 and C3 write 3, so A2 is never the last write to z. Every write that could come last is 3.

**Step 3: Final y can be 0.** In the order below, A7 takes effect after B4, so y ends as 0.
- A1 (reads x = 0)
- C1, C2, C3, C4 (x = 5)
- B1, A2 (z = 0), A3 (reads 0), A4 (x = 0)
- B2 (reads y = 0), B3 (reads x = 0), B4 (y = 4), C5 (reads 4)
- B5 (z = 3), C6 (reads 3), B6 (reads x = 0)
- A5, A6 (reads y = 0), C7 (x = 4), A7 (y = 0), A8 (reads 4)
- B7 (reads 4), B8 (reads 3)

**Step 4: Final y can be 4.** Here B4 takes effect after A7, so y ends as 4.
- A1
- C1, C2, C3, C4 (x = 5)
- B1, A2 (z = 0), A3 (reads 0), A4 (x = 0)
- A5, A6 (reads y = 0), A7 (y = 0)
- B2 (reads y = 0), B3 (reads x = 0), B4 (y = 4)
- B5 (z = 3), B6 (reads x = 0)
- C5 (reads y = 4), C6 (reads z = 3), C7 (x = 4)
- A8 (reads 4), B7 (reads 4), B8 (reads 3)

Every known read result holds in both orders.

BEGIN
0 3
4 3
END