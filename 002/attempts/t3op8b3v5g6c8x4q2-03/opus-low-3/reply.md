The final value of y is always 3. The final value of z can be 2 or 3.

**Step 1: C2 reads x = 2, so A8 must have written that 2.**
- The writes to x are A1 (1), A2 (3), B2 (5), B6 (3), C5 and A8.
- C5 comes after C2 in thread C, so it cannot supply C2's value.
- B6 writes 3, because B4 returned 3.
- So the 2 comes from A8. That means A7 read y = 2, and A8 → C2.

**Step 2: The final y is 3.**
- The writes to y are B1 (3), A4 (3), A5 (2) and B7 (3).
- C7 reads x = 3 after C5 has written 2 to x. Some write of 3 to x must take effect between C5 and C7.
  - A8 cannot be it, because A8 → C2 → C5.
  - So that write is B6, which gives C5 → B6.
- The chain is then A7 → A8 → C2 → C5 → B6 → B7.
- B7 is therefore the last write to y, and it writes 3. Final y = 3.

**Step 3: The final z can be 2 or 3.**
- The last writes to z are C8 (writes 2, C2's value) and B8 (writes 3, B4's value).
- C6 reads z = 3 after C4 has written 4. Either B5 or B8 can supply that 3 between C4 and C6.
- Both orders of the last two writes are possible:
  - If B5 supplies C6's 3 and B8 comes after C8, the final z is 3.
  - If B8 takes effect between C4 and C6, it lands before C8, and the final z is 2.

BEGIN
3 2
3 3
END