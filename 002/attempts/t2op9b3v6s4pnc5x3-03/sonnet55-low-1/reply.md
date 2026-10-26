Every operation of thread B must finish before Q, while A2 through A8 all start after Q. Only A1 is not tied to Q, apart from coming before A2.

**Thread B:**
- B1 and B2 read x, which is still 0, because A's only write to x (A5) comes after Q. So B2 = 0.
- B3 reads y. It sees 1 only if A1 took effect before B3, otherwise 0. Call this value b3.
- B4 writes 6 to z.
- B5 writes b3 to x, B6 writes B2 (0) to y, and B7 writes 6 to y.
- B8 reads y. It returns 1 only if A1 took effect after B7 and before B8. Otherwise it returns 6, because B6 and B7 overwrite any earlier A1 write.

**Thread A (all after Q):**
- A2 reads x, which is b3, since B5 wrote it and nothing else has changed it.
- A3 writes 2 to z, which overwrites B4's 6. So A7 always returns 2.
- A4 writes b3 to y, after all of B's writes. So A8 returns b3.

**Cases:**
- b3 = 1 requires A1 before B3. Then B6 and B7 overwrite y, so B8 = 6. This gives A7 = 2, A8 = 1, B8 = 6.
- b3 = 0 means A8 = 0. B8 is 6 when A1 comes before B7 or after B8, and 1 when A1 falls between B7 and B8. This gives (2, 0, 6) and (2, 0, 1).

BEGIN
2 0 1
2 0 6
2 1 6
END