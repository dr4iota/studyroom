Eight combinations are possible.

**Key facts**

- **B9:** Every A operation ends before R, and B8 and B9 come after R. B8 is therefore the last write to z before B9 reads it, so B9 returns B2's value. The final z is that same value.
- **A4, A6, A7:** B1 ends before P and A1 ends before A2, so both writes to z happen before A4 reads. A4 reads 6 or 1, depending on whether A1 or B1 wrote last. Nothing else writes z until A9, so A6 writes that value back and A7 reads it too. Call this value v, with v ∈ {1, 6}.
- **y:** Only A8 writes y, and it writes v. So the final y is v.
- **B2:** It reads y before Q, so it returns 0 (if A8 hasn't happened yet) or v (if A8 happened before B2).
- **x:** The writes are A2 (1), B5 (3), B6 (B3's value) and B7 (4). B5, B6 and B7 run in that order, so B7's 4 overwrites B5 and B6. The final x is 4 unless A2 takes effect after B7, in which case it is 1.
- **x = 1 forces B2 = 0:** B2 comes before B3, B4, B5 and B7 in thread B. If A2 comes after B7, then A8 comes after A2, so A8 comes after B2. B2 therefore reads 0.

**Combinations (Q1, Q2, Q3, Q4)**

- Final x = 4: B2 can read 0 or v, and v can be 1 or 6. This gives (0,4,1,0), (1,4,1,1), (0,4,6,0), (6,4,6,6).
- Final x = 1: B2 reads 0, and v can be 1 or 6. This gives (0,1,1,0), (0,1,6,0).

BEGIN
0 4 1 0
1 4 1 1
0 4 6 0
6 4 6 6
0 1 1 0
0 1 6 0
END