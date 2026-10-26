Values asked, in order: A1's read, B3's read, the final value of y.

**1. What the sync lines mean**
- Thread B: B1–B4 end before Q. B5 starts before P and ends after P.
- Thread A: A5 starts after Q and ends before P.
- So B4 happens before A5. B5 can take effect at any point after B4: before A1–A4, among them, or after them.
- Apart from that, each thread just runs in its own order.

**2. What A1 can return**
A1 can read 0 (no write yet), 1 (B1), 3 (B2 or B4) or 1 (B5). The possible values are 0, 1 and 3.

**3. What B3 can return**
- **3 from B2:** no A write falls between B2 and B3. A1 can be 0, 1 or 3. A1 can read 3 from B2, or from B4 if A1 comes later.
- **The value written by A2:** A2 writes A1's value, and A1 comes before B3. So A1 read 0, 1 (B1) or 3 (B2). This gives the pairs (0,0), (1,1) and (3,3).
- **2 from A4:** A1 comes before B3, so A1 is 0, 1 or 3. This gives (0,2), (1,2) and (3,2).

**4. Final value of y**
The last write to y is either A4 (2) or B5 (1). Every other write to y comes before one of these two in its own thread.
- If B3 read 2, then A4 came before B3, and B3 comes before B5. So y ends as 1.
- Otherwise A4 comes after B3. A4 and B5 can then be in either order, so y ends as 1 or 2.

BEGIN
0 3 1
0 3 2
1 3 1
1 3 2
3 3 1
3 3 2
0 0 1
0 0 2
1 1 1
1 1 2
3 3 1
0 2 1
1 2 1
3 2 1
END