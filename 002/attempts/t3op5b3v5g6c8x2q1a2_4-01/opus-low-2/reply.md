The final value of z can be **4** or **2**.

**y always stays 0.** The only write to y is B3, which writes the value B1 read from y. No write to y can take effect before B1, so B1 reads 0. B3 therefore writes 0 to y.

**Writes to z:**
- A1 writes 2.
- B2 writes 0 (the value B1 read).
- C1 writes 1.
- C2 writes 4.

**What B4 returning 4 requires:** The last write to z before B4 must be C2.
- B2 comes before B4 in thread B, so B2 must take effect before C2.
- C1 comes before C2 in thread C.
- A1 must take effect either before C2 or after B4.

**The final value of z** comes from whichever of these four writes takes effect last. B2 and C1 both come before C2, so the last write is either C2 or A1.
- If A1 takes effect before C2, the final value is 4. For example: B1, B2, B3, A1, C1, C2, B4, then the rest.
- If A1 takes effect after B4, the final value is 2. For example: B1, B2, B3, C1, C2, B4, then A1 through A5, then C3 and C4. A3 and A4 read x as 1 after A2, so the known results hold.

BEGIN
2
4
END