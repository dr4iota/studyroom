The possible outcomes are (Q1, Q2) = (0, 2) and (3, 2).

**Q2 (final z) is always 2.** A8 writes 2 and is A's last operation. The only other z-writes are A1, A5, A7, B6, and C5. Each of those is either before A8 in A's program order or forced to take effect before A8. C8 reads z = 2, which forces C5 < A8 < C8, so C5 cannot land after A8.

**Q1 (value of A4) can be 0 or 3, but not 1.**
- A6 reads z = 0, so B6 (which writes B1's value) must be 0, and A5 < B6 < A6. B1 must therefore read 0, so B1 comes before every x-write.
- B7 reads x = 3, so B7 must come before C6. Since B7 comes after B6, which comes after A5, which comes after A4, we get A4 < B7 < C6.
- Reading 1 from y would require C7 < A4 (C7 is the only y-write of 1). But C6 precedes C7 in program order, so C6 < C7 < A4 < B7 < C6, a contradiction. So A4 cannot read 1.
- Reading 3 is achieved by the schedule: B1, A1, B2, B3, C1, A2, B4, C2, C3, C4, A3, A4 (reads y = 3), B5, A5, B6, A6, B7, A7, C5, C6, C7, A8, C8. This satisfies every read and ends with y = 1 and z = 2.
- Reading 0 is achieved by the same schedule with B5 moved before A4 (after C2). A4 then reads B5's value 0, and the rest is unchanged.

BEGIN
0 2
3 2
END