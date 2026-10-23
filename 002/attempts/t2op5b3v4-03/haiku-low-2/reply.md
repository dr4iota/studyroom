Each thread's operations take effect in program order, and each read sees the latest earlier write. The three asked reads depend on different writes:

- **A1 (reads z):** Only B's writes to z can be visible, since A2 and A3 come after A1. So A1 returns 0 (before B1), 3 (after B1 but before B3), or 2 (after B3). Each is achievable with a suitable interleaving.
- **A5 (reads y):** Only B5 writes y, so A5 returns 4 if B5 comes before A5, otherwise 0.
- **B4 (reads x):** Only A4 writes x, so B4 returns 1 if A4 comes before B4, otherwise 0.

Each of the 12 combinations (3 × 2 × 2) can be realized by an interleaving that respects program order. For example:
- (3, 4, 0): b1, a1, b2, b3, b4, a2, a3, a4, b5, a5
- (2, 0, 1): b1, b2, b3, a1, a2, a3, a4, a5, b4, b5
- (0, 0, 0): a1, b1, b2, b3, b4, a2, a3, a4, a5, b5

The values are listed in the order Q1 Q2 Q3 (A1, A5, B4).

BEGIN
0 0 0
0 0 1
0 4 0
0 4 1
2 0 0
2 0 1
2 4 0
2 4 1
3 0 0
3 0 1
3 4 0
3 4 1
END