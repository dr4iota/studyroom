**Ordering from the sync points**
- Thread A's A1–A3 come before R. Thread B's B7 and B8 come after R. So A1–A3 all take effect before B7.
- Thread B's B1–B6 come before P. Thread A's A4 onward comes after P. So B1–B6 all take effect before A4.
- B8 comes before Q, and A7 comes after Q. So B8 takes effect before A7.

**B5 (read x)**
- The only writes to x are B3 (writes 4), A4 and A6.
- A4 and A6 come after P, which is after B6, so they cannot precede B5.
- B3 comes before B5 in thread B, so B5 returns 4.
- Therefore B6 writes 4 to z, and B8 will write 4 to y.

**Q1: A2 (read z)**
- The writes to z are B1 (4), B6 (4), A5 and B9.
- A5 comes after A2 in thread A. B9 comes after B8, which is after R, which is after A2. So neither can precede A2.
- A2 returns 0 if it takes effect before B1, and 4 otherwise.
- Possible values: 0 or 4.

**Q2: A3 (read x)**
- The writes to x are B3 (4), A4 and A6.
- A4 and A6 come after A3 in thread A, so only B3 can precede A3.
- Possible values: 0 or 4.

**Q3: A7 (read y)**
- The writes to y are B2 (2), B8 (4) and A8.
- A8 comes after A7. B2 comes before B8, and B8 comes before A7.
- So the last write before A7 is always B8, and A7 returns 4.

**Combinations of Q1 and Q2**
- Q1 depends only on where A2 falls relative to B1, and Q2 depends only on where A3 falls relative to B3.
- These two choices are independent. For example, A2 = 4 with A3 = 0 happens with the order B1, A1, A2, A3, B2, B3.
- So all four combinations are possible.

BEGIN
0 0 4
0 4 4
4 0 4
4 4 4
END