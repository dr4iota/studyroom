Every combination below is achievable. The asked values depend on only a few orderings.

**Q2 (B2).** B2 happens before B3 starts, so only A2 can have written y by then. B2 returns 0 (before A2) or 2 (after A2).

**Q1 (A4).** A1–A3 all end before A4 starts, so A4 sees A2's write of 2 unless B3's write of 3 takes effect first. B3 starts before P and ends after P, as does A4, so both can take effect on either side of P in either order. A4 returns 2 or 3, independently of the other values.

**Q3 (final y).** B4 runs after B3 ends and after P. A4 only reads, and A2 and B3 are earlier in every ordering, so B4's write is last. The final y is therefore the value B1 read from x: 0, 3 or 1.

**Constraints linking B1 and B2.**
- B1 = 0 (before A1): B2 can be 0 or 2.
- B1 = 3 (after A1, before A3): B2 can be 0 (before A2) or 2 (after A2).
- B1 = 1 (after A3): A2 precedes A3, which precedes B1, which precedes B2, so B2 must be 2.

The valid (B2, final y) pairs are (0,0), (2,0), (0,3), (2,3) and (2,1). Each pairs with A4 = 2 or 3.

BEGIN
2 0 0
2 2 0
2 0 3
2 2 3
2 2 1
3 0 0
3 2 0
3 0 3
3 2 3
3 2 1
END