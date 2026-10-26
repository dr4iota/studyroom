**Result:** Q1 (final y) is always 3. Q2 (final z) can be 2 or 3.

**Why final y is always 3:** Thread A's read A6 returns 2, and A7 must also read 2 for A8 to write the 2 that C2 needs. So A5 precedes A7. C2 reads x = 2, which forces A8 to be the last x-write before C2. C7 reads x = 3, and the only candidate 3-write after C5 is B6, so B6 comes after C5. Since B7 comes after B6, B7 is after A5 and is the last y-write, writing 3.

**Why final z is 2 or 3:** B4 forces C1 between B3 and B4. C6 forces B5 or B8 to fall between C4 and C6, which puts C8 after everything that matters. So the last z-write is either C8 (writes 2) or B8 (writes 3), depending on which comes later.

**Both values are achievable:**
- Order B1, B2, B3, C1, B4, A1, A2, A3, A4, A5, A6, A7, A8, C2, C3, C4, B5, C5, B6, C6, C7, B7, B8, C8 gives final z = 2.
- Moving B8 after C8 (so ..., B7, C8, B8) gives final z = 3.

I checked every read in both schedules (A3, A6, B4, C2, C6, C7) against its required value.

BEGIN
3 2
3 3
END