**Approach.** There are no sync points, so the only limits are each thread's program order and the two known read results.

**What the known reads force.**
- B2 returns 0, although B1 wrote 3 just before it in B's order. So some write of 0 must take effect after B1 and before B2.
- C2 returns 0 after C1 wrote 3, so likewise a write of 0 must fall between C1 and C2.
- The only operations that can write 0 are A2 (if A1 read 0) and A4 (if A3 read 0).

**Q1 = 0 (A3 reads 0).**
- A3 must then come before B3 and C3, and A4 writes 0.
- The last writes are B3 (2), C3 (2), C4 (3) and A4 (0).
- B4 can return 0, 2 or 3.
- No value 2 can land after B4 and after C4. So these two combinations are impossible: B4 = 0 with final 2, and B4 = 3 with final 2.
- Possible results: (0,0,0), (0,0,3), (0,2,0), (0,2,2), (0,2,3), (0,3,0), (0,3,3).

**Q1 = 2 (A3 reads 2).**
- A4 writes 2, and no write of 0 remains.
- So B4 is 2 or 3, and the final value is 2 or 3. All four pairs occur. For example, the order B3, C3, A3, C4, B4, A4 gives (2,3,2).

**Q1 = 3 (A3 reads 3).**
- A3 comes after C4, and A4 writes 3.
- B4 = 3 with final 2 would need a write of 2 after B4. But B3 comes before B4, and C3 comes before C4, which is before A3. So that case is impossible.
- Possible results: (3,2,2), (3,2,3), (3,3,3).

BEGIN
0 0 0
0 0 3
0 2 0
0 2 2
0 2 3
0 3 0
0 3 3
2 2 2
2 2 3
2 3 2
2 3 3
3 2 2
3 2 3
3 3 3
END