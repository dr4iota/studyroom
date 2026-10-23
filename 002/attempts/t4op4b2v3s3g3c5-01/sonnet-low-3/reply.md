Combinations are listed as A2, D3, final x.

**Constraints**
- C1 returns 0, so C1 takes effect before both y-writes (A1 and B3). A1 comes before A2, so A2 takes effect after C1.
- Every x-write is either followed by a later write in the same thread (D1 by D2, C3 by C4) or is a 1 or 2 written last. So the final x can only be 1 (D4 last) or 2 (C4 or B1 last). It cannot be 3.
- D3 reads y, and only 1 is ever written to y, so D3 returns 0 or 1.
- A2 can read any x value from 0 to 3, subject to the D3 check below.

**D3 and A2 interaction**
- If D3 returns 0, D3 takes effect before A1, and D1 takes effect before D3. A2 then comes after D1, so A2 cannot return 0.
- If A2 returns 0, A2 comes before D1 and D3 comes after A2. D3 is therefore after A1 and returns 1.

**Feasibility of the remaining combinations**
- For A2 = 1, 2 or 3, each of D3 = 0 and D3 = 1 can be combined with final x = 1 or 2.
- For A2 = 0, D3 = 1 can be combined with final x = 1 or 2.
  - Final 1: D4 is last.
  - Final 2: C4 or B1 is last.

BEGIN
0 1 1
0 1 2
1 0 1
1 0 2
1 1 1
1 1 2
2 0 1
2 0 2
2 1 1
2 1 2
3 0 1
3 0 2
3 1 1
3 1 2
END