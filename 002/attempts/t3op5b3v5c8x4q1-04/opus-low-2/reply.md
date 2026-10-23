**Answer: the final value of z is 4 or 5.**

**What A4 = 5 forces.** The writes to z are A1 (5), A2 (3), B2 (the value B1 read from x), B3 (4), C2 (3) and C5 (the value C4 read from z).

- A1 cannot be the write A4 sees, because A2 writes 3 after A1 and before A4.
- B2 cannot write 5. That would need B1 to read 5 from x, and only A5 writes 5 to x, which happens after A4.
- So A4 sees C5, and C4 must have read 5.
- C4 reads 5 only if A1 is the last write to z before C4. So C2 < A1 < C4 < A2.
- Since C5 comes after C4, and A2 must not sit between C5 and A4, we also get A2 < C5 < A4.
- Neither B2 nor B3 may take effect between A1 and C4, or between C5 and A4.

**Final z.** A2 takes effect before C5, so it cannot be last. B2 takes effect before B3, so it cannot be last either. The last write to z is therefore C5 (5) or B3 (4).

- **z = 5:** Run all of thread B before C2. Then C5 is the last write to z.
- **z = 4:** Run B1–B2 before everything else, and run B3 after A4. B3's value 4 is then the last write to z.

BEGIN
4
5
END