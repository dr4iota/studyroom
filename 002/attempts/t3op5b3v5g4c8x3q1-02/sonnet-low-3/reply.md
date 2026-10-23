C4 can return 1, 2 or 4.

**Forced ordering.**
- A4 returns 4, and the only write of 4 to y is C3. So C3 takes effect before A4.
- Thread A's A1 is the only other write to y, and it must come before C3. Otherwise the last write before A4 would not be 4.
- B1 returns 1, so A1 takes effect before B1. B1 must also come before C3, since after C3 y holds 4.
- Together: A1 < B1 < C3 < A4. Within each thread, C1 < C2 < C3 < C4 and A2 < A3 < A4.

**Writes to z that can matter for C4.**
- C1 writes 2, A2 writes 1, and B3 writes whatever B2 read, which is 1 or 4.
- C4 comes after C1, so it can never return 0.
- No write of 5 goes to z, since C2 writes it to x. So C4 cannot return 5.

**Which values are achievable.**
- **2:** Run A1 and A2 first, then C1. B3 takes effect after C4, or not before it. Nothing overwrites z between C1 and C4, so C4 returns 2.
- **1:** Order C1 before A2, with A2 after A1 and before C4. A2 is also constrained to precede A3 and A4. Nothing else writes z before C4, so C4 returns 1. Alternatively, B2 reads 1 (before C3) and B3 writes 1 after C1 and before C4.
- **4:** Order A1, B1, C3, then B2 reads 4, then B3 writes 4 to z, then C4. A2 and C1 both come earlier, so C4 returns 4.

BEGIN
1
2
4
END