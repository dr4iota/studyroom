The possible outcomes are **(final y, final z) = (0, 3)** and **(4, 3)**.

**Forced values:**
- A3 reads z = 0, and the only write that can precede it with value 0 is A2. So A1 must have read 0, which makes A2 write 0.
- A1 reads 0 only if C4 and C7 (the nonzero writes to x) both come after A1.
- A8 reads x = 4, which requires A4 < C7 < A8.
- B8 reads z = 3, which requires the last z-write before B8 to be 3 (B5 or C3).

**Final z:**
- C2 is always overwritten by C3, and C1 by C2, so 4 and 5 are impossible.
- B1 always precedes B5, so 2 is impossible.
- Final z = 0 would require A2 to come after the last 3-write. But A2 < A4 < C7 < B7 < B8, so B8 would read 0, contradicting B8 = 3.
- So final z = 3 (C3 or B5 is last).

**Final y:** The last y-write is A5 or A7 (both 0) or B4 (4). Since C5 reads y = 4, A5 and A7 cannot fall between B4 and C5, and B4 cannot fall between A5 and A6. This leaves two cases:
- **A7 before B4:** final y = 4. Example order: A1–A7, then B1–B6, then C1–C7, then B7, B8, A8. This gives final z = 3 from C3.
- **A7 after C5:** final y = 0. Example order: A1–A6, then B1–B6, then C1–C7, then A7, then B7, B8, A8. This gives final z = 3 from C3.

BEGIN
0 3
4 3
END