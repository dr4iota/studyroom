**Values over time.** Thread B does not write until after B3. So B1, B2 and B3 all see some point in A's sequence of values for x: 0 → 2 → 3 → 1 → 3. B's reads happen in order, so B2 sees a point at or before the point B3 sees. Let v be the value B2 returns, which B4 and B5 both write.

**Q1 (A5).** A5 returns one of two things:
- **3**, from A4, if no B write takes effect between A4 and A5. This can always happen, for example if B's writes come before A4 or after A5.
- **v**, if B4 or B5 takes effect after A4 and before A5.

**Q2 (B3).** B3 returns whatever value A's sequence holds at that moment: 0, 2, 3 or 1.

**Combining the cases:**
- **A5 = 3:** B3 can be any of 0, 2, 3, 1. This gives (3,0), (3,2), (3,3), (3,1).
- **A5 = v:** B3 must see the same point as B2 or a later one.
  - v = 0 (initial value): B3 ∈ {0, 2, 3, 1}
  - v = 2: B3 ∈ {2, 3, 1}
  - v = 3 (first 3, from A2): B3 ∈ {3, 1, 3}
  - v = 1: B3 ∈ {1, 3}
  - v = 3 (second 3, from A4): B3 = 3

BEGIN
0 0
0 2
0 3
0 1
2 2
2 3
2 1
3 0
3 2
3 3
3 1
1 1
1 3
END