Q1 is always 1, and Q2 can be 3 or 5.

**Q1 (A6 reads y):** The only y-write with value 2 is C3, and A3 must see it, so C2 < C3 < A3. A4 (writes 1) sits between A3 and A6 in thread A's order, and no other y-write can land between A4 and A6, so A6 always returns 1.

**Q2 (final z):**
- C8 reads z = 3, and the only write that can produce 3 is B8 (writing B3's value). So B3 returns 3, B8 < C8, and C6 < B8 (C6 precedes C8 in thread C).
- B4 reads z = 2, so A1 < B4 with no overwrite in between. A2 must come after B4 (it either lands before B8 or after C8). Final z = 1 would need C6 after B8, which contradicts C6 < B8.
- Final z = 3 is achievable with A2 between B4 and B8. Final z = 5 is achievable with A2 after C8.

Both cases are consistent with the x reads (B2, B3, A7 all see 3) and with final x = 3, since C4 and C5 always precede C7 and every other x-write is 3.

BEGIN
1 3
1 5
END