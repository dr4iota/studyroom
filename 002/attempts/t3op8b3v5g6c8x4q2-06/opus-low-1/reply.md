**Answer:** A4 can return 0 or 3, and the final value of z is always 2. Each step below rules out orderings using a read's known result.

**1. A6 read z = 0, so B1 read 0.**
- A1 (2) and A5 (4) both write z before A6. So the last z write before A6 must write 0.
- The only write that can write 0 is B6, and only if B1 read 0.
- So B1 returned 0, and A5 < B6 < A6, with no other z write between B6 and A6.
- B5 also writes 0 to y. Since y ends at 1, C7 must come after B5.

**2. B2 and B3 read z = 2.**
- They come before B6, so before A6 and A8. They must therefore read A1's 2.
- This gives A1 < B2, B3 < A5 < B6 < A6.

**3. Reads of x.**
- B1 read 0, so B1 comes before A2 and before C1.
- B4 read 1, so B4 follows A2 with no 3 or 4 written to x in between.
- B7 read 3, so a 3 from C1 or C3 is written after B4, and C6 has not yet run before B7. So B4 < (C1 or C3) < B7 < C6.

**4. C8 read z = 2, so the final z is 2.**
- If C8 read A1's 2, C5 would come before A1. Then C1 and C3 would also be before A1, and before A2 and B4. No 3 could then be written after B4, which contradicts B7.
- So C8 reads A8's 2. That means A8 is the last z write before C8, and C5 comes before A8.
- After A8, no z write remains, so z ends at 2.

**5. What A4 can read from y.**
- The y writes are C2 (3), B5 (0) and C7 (1). A4 comes before A5 and B6.
- **1 is impossible.** C7 comes after C6, which comes after B7, which comes after B6, which comes after A5, which comes after A4. So C7 is always after A4.
- **3 is possible:** C2 < A4 < B5.
- **0 is possible** in two ways:
  - Before any y write: B4 < C1 < A3 < A4 < C2, where C1 supplies the 3 that A3 reads.
  - From B5: B5 < A4 < A5, with C2 not between B5 and A4.

BEGIN
0 2
3 2
END