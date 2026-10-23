Only the order of whole operations matters here, since no operation has a sync line. Let b be the value B1 reads. B3, B4 and B5 all write b.

**Which values are possible**
- b can be 0, 2 or 4. It is 0 only if B1 runs before any write to z.
- A3 always reads 4 or 2, because A1 has already written 4 and C1 only writes 2. So A5 writes 4 or 2, and z is never 0 after the first write.
- C5 runs after C1, so it reads 2 or 4. Both are achievable.
- A4 reads y, which is 0 until B4 runs and b afterwards. So A4 is 0 or b.
- B2 is always followed by B3, so x = 4 at the end only when b = 4 and B3 is the last write to x. Otherwise the final x is b (B3 last) or 2 (C2 last).

**Case b = 0** (B1 runs first)
- y only ever holds 0, so A4 = 0.
- Final x is 0 (B3 after C2) or 2 (C2 last).
- C5 is 2 or 4 in either case.
- This gives (0,2,0), (0,4,0), (0,2,2), (0,4,2).

**Case b = 2**
- A4 is 0 or 2.
- Final x is 2, since both B3 and C2 write 2.
- C5 is 2 or 4.
- This gives (0,2,2), (0,4,2), (2,2,2), (2,4,2).

**Case b = 4**
- A4 is 0 or 4.
- Final x is 4 (B3 last) or 2 (C2 last).
- C5 is 2 or 4.
- All eight combinations are achievable. For example, A1, A2, B1, B2, C1, C2, B3, B4, A3, A4, A5, then the rest of C gives A4 = 4, C5 = 2 and x = 4.
- This gives (0,2,2), (0,4,2), (0,2,4), (0,4,4), (4,2,2), (4,4,2), (4,2,4), (4,4,4).

BEGIN
0 2 0
0 4 0
0 2 2
0 4 2
0 2 4
0 4 4
2 2 2
2 4 2
4 2 2
4 4 2
4 2 4
4 4 4
END