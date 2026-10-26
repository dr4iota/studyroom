Both A2 and A3 can see several values, so I enumerate by what A3 reads. A3's value v is always the latest B write before A3, because A4 comes after A3.

**Constraints**
- B2 ends before P, and A2 ends after P. A3 starts after A2 ends, so A3 comes after B2 and cannot read 0.
- A2 takes effect at one instant between its start and end. It can take effect before B2, which gives 0. It can also take effect later, as long as it is before A3.
- Writes to x by B occur in the order 3, 2, 1. A4 writes v after A3, and it can land anywhere after A3 in that sequence.

**Case A3 = 3** (A3 sees B2 only)
- A2 can be 0 or 3.
- A4 writes 3. If it lands before B4, B4 overwrites it and x ends at 1. If it lands after B4, x ends at 3.
- Outcomes: (0,3,1), (0,3,3), (3,3,1), (3,3,3).

**Case A3 = 2** (A3 sees B3, before B4)
- A2 can be 0, 3 or 2.
- A4 writes 2. If it lands before B4, x ends at 1. If it lands after B4, x ends at 2.
- Outcomes: A2 in {0,3,2} with final in {1,2}.

**Case A3 = 1** (A3 sees B4)
- A2 can be 0, 3, 2 or 1.
- A4 writes 1, so the final value is 1.
- Outcomes: A2 in {0,3,2,1} with final 1.

BEGIN
0 3 1
0 3 3
3 3 1
3 3 3
0 2 1
0 2 2
3 2 1
3 2 2
2 2 1
2 2 2
0 1 1
3 1 1
2 1 1
1 1 1
END