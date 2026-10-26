Both D3 values and both final values are possible. A2 can be 0, 1, 2 or 3, except that A2 = 0 cannot occur together with D3 = 0.

**Constraints**
- C1 reads y as 0, so C1 happens before the first write to y. A1 and B3 are the only writers of y, and both write 1. C1 therefore happens before A1 and before B3.
- C2 ends before P and B3 is after P, so C2 takes effect before B3.
- C4 is before Q and B1 is before B2's start, which is before Q, so every write by B and C except possibly later D writes happens before Q.

**Q3 (final x)**
- The last write cannot be 3. C3 is always followed by C4 (value 2), and D1 (value 3) is followed by D2 and D4 (value 1).
- Final x = 1 is possible when D4 is the last write.
- Final x = 2 is possible when D4 comes before C4 or B1, so one of them is the last write.

**Q2 (D3)**
- D3 = 1 is possible when D3 comes after A1.
- D3 = 0 requires D3 before A1 and before B3. Then D1 and D2 come before D3, and A2 comes after A1.

**Q1 (A2)**
- A2 = 0 requires A2 before every write to x. D3 is after D1, so D3 is also after A2, which is after A1. That forces D3 = 1.
- If D3 = 0, D1 and D2 have already written before A2, so A2 cannot be 0. A2 can still be 1 (from D2 or D4), 2 (from B1), or 3 (from C3, with C4 after A2).
- If D3 = 1, A2 can be 0, 1, 2 or 3.

For every allowed (A2, D3) pair, both final values 1 and 2 can be arranged.

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