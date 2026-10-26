Only y = 1 is possible.

Block x is written by A1 (1), A2 (4), B3 (5), B4 (2) and C4 (the value C1 read). For x to end at 4, the last write to x must be either A2, or C4 with C1 having returned 4.

**Case 1: A2 is the last write to x.**
- A2 must come after B3 and B4, and B2 comes before B3 in thread B, so B2 < B3 < B4 < A2.
- A3 comes after A2 in thread A, so A3 comes after B2.
- A3 is therefore the last write to y, and the final y is 1.
- This is achievable: B1, B2, B3, B4, A1, A2, A3, then C reads z = 3 for C2 (B1 wrote 3), and the remaining operations do not affect y.

**Case 2: C4 is the last write to x, and C1 returned 4.**
- The only way z can hold 4 is for A5 to write it, which needs A4 to have read y = 4, so B2 < A4.
- C2 must later return 3. The only write of 3 that can happen after A5 is C3, but C3 depends on C2 having already read 3, so it cannot supply the value. That leaves B1.
- Thread B orders B1 before B2, and B2 is before A4, which is before A5. So B1 is before A5, and no 3 is written after A5. C2 cannot return 3, which contradicts the known result.
- This case is impossible.

So only Case 1 occurs, and the final y is 1.

BEGIN
1
END