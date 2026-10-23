Only one operation writes y: B2 writes 4. So A1 can return 0 (A1 happens before B2) or 4 (A1 happens after B2). A4 reads y, but its result affects none of the asked values.

**Q1 (A1):** Both 0 and 4 are possible. In either case the A operations that write x can be ordered freely relative to B3, B5 and the rest of thread B. There are no sync points, and the only other constraint is that B1 returned 0, which holds as long as it happens before B2.

**Q2 (B3):** B3 runs after B2 and before B5, and it reads whichever write to x took effect last before it.
- It returns 0 if it happens before A2.
- It returns 2 if it happens after A2 and before A3, or after A5.
- It returns 4 if it happens after A3 and before A5.
- B5 comes after B3 in thread B, so B5 never affects B3.

All three values (0, 2, 4) are available whether A1 returned 0 or 4. If A1 returned 4, B2 comes first and then the A writes follow, but B3 can still run before A2.

**Q3 (final x):** The last write to x is either A5 (value 2) or B5 (value 4).
- Final 4 requires B5 after A5.
- Final 2 requires A5 after B5.

Either ordering is compatible with every B3 value above. For final 2, B3 returns 0, 2 or 4 and A5 is delayed until after B5. For final 4, A5 happens before B5.

All 2 × 3 × 2 = 12 combinations are therefore possible.

BEGIN
0 0 2
0 0 4
0 2 2
0 2 4
0 4 2
0 4 4
4 0 2
4 0 4
4 2 2
4 2 4
4 4 2
4 4 4
END