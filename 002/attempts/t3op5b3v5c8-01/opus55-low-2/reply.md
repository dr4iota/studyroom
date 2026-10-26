Every combination below is possible: 14 in total.

**Which values each block can hold**
- z only ever receives 4 (A1, A2), 2 (C1), or whatever A3 read. So z can only hold 0, 2 or 4.
- Let v be the value B1 reads from z. Then v is 0, 2 or 4.
- y only ever receives v (from B4 and B5), so A4 returns 0 or v.
- C5 runs after C1, and z is never set back to 0, so C5 returns 2 or 4.
- B2 takes effect before B3 in thread B. So the final x is the later of B3 (writes v) and C2 (writes 2). It is therefore v or 2.

**Case v = 0** (B1 takes effect before both A1 and C1)
- A4 returns 0, because y can only ever hold 0.
- C5 can be 2 (C1 is the last write to z before C5) or 4 (A1 or A2 is).
- Final x can be 0 (B3 after C2) or 2 (C2 after B3).
- All 4 combinations occur, since after B1 the other operations can be ordered freely.

**Case v = 4** (A1 takes effect before B1, and C1 does not fall between them)
- A4 can be 0 (A4 before B4) or 4 (A4 after B4).
- C5 can be 2 or 4:
  - For 2, C1 comes after all of thread A, so it is the last write to z before C5.
  - For 4, C1 comes early and thread A's writes of 4 come after it, before C5.
- Final x can be 4 or 2, depending on the order of B3 and C2.
- These choices do not interfere with each other, so all 8 combinations occur.

**Case v = 2** (C1 is the last write to z before B1)
- Final x is 2 whichever of B3 and C2 is later, since both write 2.
- A4 can be 0 (A4 before B4) or 2 (A4 after B4).
- C5 can be 4 (an A write of 4 is last before C5) or 2.
- C5 = 2 together with A4 = 2 also works. Order: C1 after A2, then A3 (returns 2), then B1 (returns 2), B4, A4 (returns 2), and A5 writes 2 to z before C5.
- So all 4 combinations occur.

BEGIN
0 2 0
0 2 2
0 4 0
0 4 2
0 2 4
0 4 4
4 2 2
4 2 4
4 4 2
4 4 4
2 2 2
2 4 2
END