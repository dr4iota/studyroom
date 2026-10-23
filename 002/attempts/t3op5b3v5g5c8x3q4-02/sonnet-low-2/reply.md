A2 is always 0, because the only write to y is A3 (writing 4), and A3 comes after A2 in the same thread.

C3 reads y, so it returns 0 if it takes effect before A3 and 4 if it takes effect after A3.

A4 reads x. The writes to x are B1 (writes 4), C1 (writes 3) and C4 (writes the value C3 read, which is 0 or 4). A1 and C2 both returned 3, so C1 took effect before A1, and x still held 3 at A1 and C2.

- **A4 = 3:** B1 happens before C1, and C4 happens after A4. This works with C3 = 0 (C3 before A3) or C3 = 4 (A3 before C3).
- **A4 = 4:** B1 happens after A1 and C2, and before A4. This works with C3 = 0 or 4.
- **A4 = 0:** only C4 can write 0, and only when C3 = 0. Take the order B1, C1, A1, C2, C3 (reads 0), C4 (writes 0), A3, A4. This is possible only with C3 = 0.
- **A4 = 0 with C3 = 4:** impossible, since nothing then writes 0 to x.

BEGIN
0 3 0
0 3 4
0 4 0
0 4 4
0 0 0
END