Each thread's A1 read decides which value A writes later, so I split on v, the value returned by A1.

**Case v = 0.** A1 reads x before C1 writes 1, so A writes 0 to z, x and finally y.
- Q1 (B2): A2 writes 0 to z and C3 writes 3, so B2 is 0 or 3. It cannot be 1, because nothing writes 1 to z in this case.
- Q2 (C2): y can hold 0 (initially, or after A5), 2 (after B1) or 3 (after A4). It cannot hold 1.
- Q3 (final y): A5 writes 0 after A4. B1 can come before A5, giving 0, or after A5, giving 2.
- Every combination of these values has a valid interleaving, for example A4, C2, A5, B1 for C2 = 3 with final y = 2.

**Case v = 1.** C1 happens before A1, so A writes 1 to z, x and finally y.
- Q1 (B2): z can be 0 (before A2 and C3), 1 (after A2) or 3 (after C3). B2 cannot be 2.
- Q2 (C2): y can be 0, 2, 3 or 1. The value 1 needs A5 before C2.
- Q3 (final y): A5 writes 1 after A4. B1 can come before A5, giving 1, or after A5, giving 2.
- Every combination of these values again has a valid interleaving. For C2 = 3 with final y = 2, B1 is placed after C2.

The answer is the union of both cases.

BEGIN
0 0 0
0 0 1
0 0 2
0 1 1
0 1 2
0 2 0
0 2 1
0 2 2
0 3 0
0 3 1
0 3 2
1 0 1
1 0 2
1 1 1
1 1 2
1 2 1
1 2 2
1 3 1
1 3 2
3 0 0
3 0 1
3 0 2
3 1 1
3 1 2
3 2 0
3 2 1
3 2 2
3 3 0
3 3 1
3 3 2
END