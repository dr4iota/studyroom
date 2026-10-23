B4 can return **0** or **4**.

**Step 1: B1 returns 0.**
- B5 returns 0 for z, and C5 is the only write to z. So C5 takes effect after B5.
- B1 comes before B5 in thread B, so B1 also takes effect before C5. It therefore reads z = 0.
- That means B3 writes 0 to x.

**Step 2: what B4 can see.** The writes to y are A1 (4), C4 (4) and A4 (whatever A3 read from z).
- A3 can read z = 3 only if it takes effect after C5. C5 is after B5, which is after B4. So if A4 writes 3, that write lands after B4 and B4 cannot see it.
- B4 can therefore only see 4 (from A1 or C4) or 0 (from A4 when A3 read z = 0).

**Step 3: B4 = 4 is possible.**
1. C1 writes 4 to x.
2. C2 writes 3 to x.
3. A1 writes 4 to y.
4. A2 reads x = 3.
5. C3 reads y = 4.
6. B1 reads z = 0.
7. B2 reads y = 4.
8. B3 writes 0 to x.
9. B4 reads y = 4.
10. B5 reads z = 0.
11. C4 writes 4 to y.
12. C5 writes 3 to z.
13. A3 reads z = 3.
14. A4 writes 3 to y.

All known results hold: A2 = 3, B2 = 4, C3 = 4, B5 = 0.

**Step 4: B4 = 0 is possible.**
1. C1 writes 4 to x.
2. C2 writes 3 to x.
3. A1 writes 4 to y.
4. A2 reads x = 3.
5. C3 reads y = 4.
6. B1 reads z = 0.
7. B2 reads y = 4.
8. A3 reads z = 0.
9. A4 writes 0 to y.
10. B3 writes 0 to x.
11. B4 reads y = 0.
12. B5 reads z = 0.
13. C4 writes 4 to y.
14. C5 writes 3 to z.

All known results hold here too.

BEGIN
0
4
END