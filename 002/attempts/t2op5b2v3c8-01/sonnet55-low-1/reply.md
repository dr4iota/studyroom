Operations are atomic, so every outcome comes from an interleaving of the two sequences. A3 reads x after A2, so it sees 1 or a value written by B3 or B4. Only the first B1 value of 0 can be rewritten later, because B3 and B4 write back whatever B1 and B2 read.

- **B1=0, B2=0:** A3 reads 1, or 0 if B3 writes 0 after A2. So y is 0 or 1.
- **B1=0, B2=3:** A1 falls between B1 and B2. A3 can read 1, 0 (after B3), or 3 (after B4). So y is 0, 1 or 3.
- **B1=0, B2=1:** A3 can read 1 or 0 (after B3 and before B4). So y is 0 or 1.
- **B1=3, B2=3:** A3 reads 1, or 3 after B3 or B4 writes 3. So y is 1 or 3.
- **B1=3, B2=1:** A3 reads 1, or 3 after B3 and before B4. So y is 1 or 3.
- **B1=1, B2=1:** B3 and B4 only write 1, so y is 1.

BEGIN
0 0 0
0 0 1
0 3 0
0 3 1
0 3 3
0 1 0
0 1 1
3 3 1
3 3 3
3 1 1
3 1 3
1 1 1
END