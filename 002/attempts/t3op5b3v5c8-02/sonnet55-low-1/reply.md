The operations have no sync points, so every outcome comes from some interleaving of the three threads' operation orders.

**Value that reaches y.** Only B4 writes y, and it writes what B3 read from z.
- B3 reads 4 if C1 does not fall between B2 and B3. It reads 2 if C1 does fall there.
- So y is 0 until B4, then holds v, where v is 2 or 4.
- A3 and C3 can each return 0 (before B4) or v (after B4).

**Final x.** The last write to x is one of B1 (writes 3), C2 (writes 2), A4 (writes A2's value) or C4 (writes C3's value). C2 can never be last, because C4 always comes after it.

- **Final x = 3.** B1 must come after C4 and A4. B4 comes after B1, so C3 and A3 must both read before B4 and return 0. This gives (0,0,3). No other pair can end with 3.
- **Final x = 0.**
  - C4 last with C3 = 0: A3 can be 0 or v, giving (0,0,0), (2,0,0), (4,0,0).
  - A4 last with A2 = 0, so A3 = 0 and C3 = 0 or v: this gives (0,0,0), (0,2,0), (0,4,0).
  - Both C3 = v and A3 = v with final 0 are also possible: A2 = 0, A3 = v, and A4 comes last. This gives (2,2,0) and (4,4,0).
- **Final x = v.**
  - C4 last with C3 = v: A3 can be 0 or v, giving (0,v,v) and (v,v,v).
  - A4 last with A2 = v, so A3 = v: C3 can be 0 or v, giving (v,0,v) and (v,v,v).

BEGIN
0 0 0
0 0 3
2 0 0
4 0 0
0 2 0
2 2 0
0 4 0
4 4 0
0 2 2
2 2 2
0 4 4
4 4 4
2 0 2
4 0 4
END