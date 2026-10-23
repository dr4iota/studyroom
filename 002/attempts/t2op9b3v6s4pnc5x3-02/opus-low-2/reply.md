**Answer: four combinations are possible, (A2, A3, A7) ∈ {0 0 4, 0 4 4, 4 0 4, 4 4 4}.**

**Ordering constraints from the sync points**

- B1 through B6 happen before P, and A4 starts after P. So every operation from A4 onward comes after B6.
- A1 through A3 happen before R, and B7 starts after R. So A1, A2 and A3 come before B7.
- B8 happens before Q, and A7 starts after Q. So A7 comes after B8.

**What B5 reads**

- The writes to x are B3, A4 and A6.
- A4 and A6 come after B6, so neither can come before B5.
- B3 comes before B5 in thread B, so B5 returns 4.
- Therefore B6 writes 4 to z, and B8 writes 4 to y.

**Q1: what A2 returns (reads z)**

- B9 comes after B7, which comes after A2, so B9 cannot affect A2.
- A5 comes after A2 in thread A.
- The only writes to z that can come before A2 are B1 (4) and B6 (4).
- So A2 returns 0 if it takes effect before B1, and 4 otherwise.

**Q2: what A3 returns (reads x)**

- The only write to x that can come before A3 is B3 (4).
- So A3 returns 0 if it takes effect before B3, and 4 otherwise.

**Q3: what A7 returns (reads y)**

- A7 comes after B8, and B8 comes after B2 in thread B. A8 comes after A7.
- So the last write to y before A7 is always B8, and A7 returns 4.

**Combining Q1 and Q2**

All four pairs are possible:
- (0, 0): A1, A2 and A3 all take effect before B1.
- (0, 4): A2 takes effect before B1, and A3 after B3.
- (4, 0): A2 and A3 both take effect after B1, and A3 before B3.
- (4, 4): A2 and A3 take effect after B3.

Each of these orderings also satisfies the constraints above.

BEGIN
0 0 4
0 4 4
4 0 4
4 4 4
END