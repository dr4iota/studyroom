Both outcomes are achievable, and the final value of z is always 3.

**Forced values:** A5 writes A1's value to y, and A6 reads y as 0 right after it, so A1 must have read 0. Then A4 and A5 and A7 all write 0, and the only other writes are 4 (B4 to y, C7 to x), 5 (C4 to x), and the z-writes 2, 3, 4, 5, 3.

**Final z = 3 only:** Each other candidate is ruled out by thread order:
- 0 (A2 last): B8 reads 3, so a 3-write must land after A2 and before B8. A2 can't be last.
- 2 (B1 last): B5 comes after B1 and before B8, so B1 can't be last.
- 4 (C1 last) and 5 (C2 last): C3 comes after both in thread C.

**Final y = 0 or 4:** Both are reachable:
- Final 4: B4 writes last. Order: B1, B2, B3, A1, A2, A3, A4, A5, A6, A7, B4, B5, B6, C1, C2, C3, C4, C5, C6, C7, B7, B8, A8. Every read checks out, and y ends at 4.
- Final 0: A5, A6, A7 move after C5, so A7 is the last y-write. Order: B1, B2, B3, A1, A2, A3, A4, B4, B5, B6, C1, C2, C3, C4, C5, C6, C7, B7, B8, A5, A6, A7, A8. Every read checks out, and y ends at 0.

Values are listed as final y, then final z.

BEGIN
0 3
4 3
END