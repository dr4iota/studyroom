Only A3 writes z, so A2 reads 0 before A3, and B5 reading 4 means A3 takes effect before B5. B1 reads 0, so B1 precedes both B2 and A5.

**x timeline without A5:** x holds 0 until B2, then 2 (B2), 1 (B3), 2 (B4). A5 writes 3 only after A4.

**Q1 (A1):** A1 is before A5, so it cannot return 3. It can return 0, 2 or 1. It can return 2 after B4, because B5 only has to come after A3.

**Q2 (A4):** A4 is before A5, so it also cannot return 3. It returns whatever x holds at its instant, so it is at or after A1's position on the timeline.

**Q3 (final x):** The last write is either B4 (final 2) or A5 (final 3).
- **Final 3 (A5 after B4):** A1 and A4 can be any pair of timeline positions with A1 no later than A4. This gives (0,0), (0,2), (0,1), (2,2), (2,1), (1,1), (1,2).
- **Final 2 (A5 before B4):** A4 is before A5, which is before B4, so A4 cannot see B4's 2 as the last write. A4 is limited to the states 0, 2, 1, giving (0,0), (0,2), (0,1), (2,2), (2,1), (1,1). The case (1,2) is excluded, since A4 would have to read B4's 2.

BEGIN
0 0 2
0 0 3
0 2 2
0 2 3
0 1 2
0 1 3
2 2 2
2 2 3
2 1 2
2 1 3
1 1 2
1 1 3
1 2 3
END