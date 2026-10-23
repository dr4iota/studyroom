Only three values are possible for C4: 1, 2, and 4. The value 0 is impossible because C1 (write 2 to z) always precedes C4 in program order.

**Forced ordering from the known reads:**
- A4 returns 4, and the only writes to y are A1 (value 1) and C3 (value 4), so A1 < C3 < A4.
- B1 returns 1, so B1 comes after A1 and before C3: A1 < B1 < C3.
- B2 follows B1, so B2 reads 1 if B2 < C3, or 4 if B2 > C3. Call its value v, which is 1 or 4.

**Possible sources for C4's read of z**, which is the last z-write before C4. The candidates are C1 (value 2), A2 (value 1), and B3 (value v):

- **2 (from C1):** Schedule A1, B1, C1, C2, C3, C4, then A2, A3, A4 (reads 4). C4 reads 2, A2 comes later, and A4 still reads 4.
- **1 (from A2):** Schedule A1, B1, C1, C2, A2, C3, C4, with B3 placed after C4. C4 reads 1.
- **4 (from B3 with v = 4):** Schedule A1, B1, C1, C2, C3, B2 (reads 4), B3 (writes 4 to z), C4 (reads 4), then A2, A3, A4 (reads 4). Works.
- **1 (from B3 with v = 1):** Schedule A1, B1, B2 (reads 1), C1, C2, C3, B3 (writes 1 to z), C4 (reads 1). Also gives 1, which is already counted.

BEGIN
1
2
4
END