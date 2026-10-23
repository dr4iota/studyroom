Y ends as 0 or 4, and z ends as 3 or 0; the achievable pairs are (0,0), (0,3) and (4,3).

**Forced facts**
- A3 reads z as 0, and A2 wrote A1's value to z just before it. Every other write to z is nonzero (2, 3, 4, 5), so A2 must be the last write to z before A3 and must have written 0. Hence A1 read 0, and A2, A4, A5, A7 all write 0.
- A8 reads x as 4. The only write of 4 to x is C7, which writes C5's value. C5 read 4, so B4 (the only 4 written to y) comes before C5.
- B2 reads y as 0, so B2 comes before B4.
- No write to z (B1, B5, C1–C3) can fall between A2 and A3.

**Final y**
- The writes to y are A5 (0), A7 (0) and B4 (4). The final y is 4 if B4 is last, and 0 if A7 comes after B4.

**Final z**
- B1 comes before B5, and C1, C2, C3 end with 3, so without A2 the last write is 3.
- The final z can also be 0 if A2 happens after B5 and C3. That works if B8 and C6 have already read 3 before A2, and A3 then reads 0 as required.

**Which pairs occur**
- **y = 4, z = 3:** run A1–A7 early, before B4, so A7 is not the last write to y. Then B4, C5, C7, A8 follow, and z ends at 3. This is consistent with all the known reads.
- **y = 0, z = 3:** the same schedule with A7 after B4.
- **y = 0, z = 0:** A2 comes after B5, B8, C3 and C6. B4 is before B5, so B4 is before A2, and A7 comes after A2, so A7 is after B4. This gives y = 0 and z = 0.
- **y = 4, z = 0 is impossible:** z = 0 needs A2 after B5, which is after B4, so A7 is after B4 and y ends at 0.

BEGIN
0 0
0 3
4 3
END