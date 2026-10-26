Writes to x are C1 (1), C2 (3), A2 (2) and B3 (3).

**Constraint from C3.** C3 returns 2, so the last write to x before C3 is A2. Hence C1 and C2 both take effect before A2, and A2 takes effect before C3. B3 either takes effect before A2 or after C3.

**A1.** A1 is a read of x that ends before A2 takes effect, so it can return 0, 1 or 3. It cannot return 2, because the only write of 2 is A2 itself.

**Case 1: B3 after C3.** The write order is C1, C2, A2, C3, B3, and the final x is 3.
- B1 only has to come before B3, so it can return 0 (before C1), 1 (between C1 and C2), 3 (between C2 and A2) or 2 (after A2).
- A1 can return 0, 1 or 3.
- The two reads are independent, so all 12 combinations of A1 and B1 are possible.

**Case 2: B3 before A2.** The final x is 2, because A2 is the last write.
- B1 comes before B3, which comes before A2, so B1 can return 0, 1 or 3 but not 2.
- A1 can return 0, 1 or 3.
- All 9 combinations are possible.

BEGIN
0 0 3
0 1 3
0 3 3
0 2 3
1 0 3
1 1 3
1 3 3
1 2 3
3 0 3
3 1 3
3 3 3
3 2 3
0 0 2
0 1 2
0 3 2
1 0 2
1 1 2
1 3 2
3 0 2
3 1 2
3 3 2
END