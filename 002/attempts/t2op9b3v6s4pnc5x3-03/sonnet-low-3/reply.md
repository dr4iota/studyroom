Every B step ends before Q, and every A step from A2 onward starts after Q, so all of B runs before A2. A1 is the only A step that can overlap B.

**What B reads**
- Only B5 and A5 write x, and A5 comes after all of B. So B1 and B2 read 0.
- B3 reads y, which is 0 or 1 depending on whether A1 has taken effect yet. Call this value v.
- B5 writes v to x.

**What A reads**
- A2 runs after all of B, so it reads x = v.
- A3 writes 2 to z. B4 wrote z earlier, and nothing else writes z later. A7 comes after A3 in A's order, so A7 = 2.
- A4 writes v to y. Nothing writes y after that, because all of B is already done. A1 precedes A4, so A4 is the last write to y. A8 comes after A4, so A8 = v.

**What B8 reads**
- B7 writes 6 to y just before B8.
- The only way B8 sees something else is if A1 (writing 1) takes effect between B7 and B8.
- If v = 1, A1 must come before B3, so B8 = 6.
- If v = 0, A1 can come after B3. It can fall between B7 and B8 (B8 = 1) or after B8 (B8 = 6).

**Possible (A7, A8, B8) combinations**
- v = 1: (2, 1, 6)
- v = 0: (2, 0, 6) and (2, 0, 1)

BEGIN
2 1 6
2 0 6
2 0 1
END