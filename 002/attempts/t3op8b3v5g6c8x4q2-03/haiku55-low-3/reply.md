Final y is always 3, and final z can be 2 or 3.

**Fixed by the known results:** B4 always reads 3, C2 always reads 2, and A3, A6, C6, and C7 return their stated values. Because C2 must read 2, the only earlier write of 2 to x is A8, so A7 must read 2 and A8 must come before C2.

**Final y:** The writes to y are A4 (3), A5 (2), B1 (3), and B7 (3). Final y = 2 would require B7 to come before A5. But C7 reading 3 forces C5 < B6 < C7 in time, and B6 precedes B7 in thread B. Chaining these gives B7 > B6 > C5 > C2 > A8 > A5, a contradiction. So B7 comes after A5, and final y is always 3.

**Final z:** Thread C's last write C8 comes after C4, so 4 can never be final, and B5 and B8 come after B3 and C3 in thread B's order, so neither 2 nor 3 can be ruled out by program order alone. Final z = 3 happens when B8 is last, and final z = 2 when C8 is last after B8. Both are realized by these interleavings:

- B1, B2, B3, C1, A1, A2, A3, A4, A5, A6, A7, A8, B4, C2, C3, C4, C5, B5, C6, B6, C7, C8, B7, B8 → final z = 3
- same up to C7, then B7, B8, C8 → final z = 2

Both respect all program orders and all known read results.

BEGIN
3 2
3 3
END