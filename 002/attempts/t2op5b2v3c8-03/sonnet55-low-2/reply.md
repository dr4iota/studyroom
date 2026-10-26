Method: B1 reads some v ∈ {0, 2, 1}, B2 writes x = v, and A4 writes x = 3 at some instant.

- **B3** reads v, unless A4 falls between B2 and B3, in which case it reads 3.
- **B5** reads x after B3:
  - If B3 = 3, then B5 = 3, because A4 has already happened and B2 is before B3.
  - If B3 = v, then B5 = v if A4 has not yet taken effect, or 3 if A4 falls between B3 and B5.
- **Final y** is decided by the later of A5 and B4:
  - If A5 is last, y = 1.
  - If B4 is last, y = B3's value. This needs A5 before B4, so A4 is also before B4.
  - If B5 = v with B3 = v, A4 is either before B2 (A5 can then be before B4) or after B5 (A5 is then after B4, so y = 1). Both cases are possible.
  - If B3 = 3, y = 3 or 1.
  - If B3 = v, y = v or 1.
  - For v = 1, y = 1 either way.

BEGIN
0 0 0
0 0 1
0 3 0
0 3 1
2 2 2
2 2 1
2 3 2
2 3 1
1 1 1
1 3 1
3 3 3
3 3 1
END