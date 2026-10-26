Every combination below comes from tracing the reads and writes by hand.

**Possible values of the reads**

- **B2:** B2 reads y after B1 (B1 wrote 2), so it returns 2, or 1 if C4 takes effect between B1 and B2. Call this value b, so b ∈ {1, 2}.
- **A3 (Q1):** A3 can see no write to y yet, B1, B3 (which writes b) or C4. So a ∈ {0, 1, 2}.
- **C1:** C1 can see 0, 1 (A1), 3, a (A4) or b (B4/B5). Call this value c.

**Final y (Q3)**

The last write to y is B3 (writes b) or C4 (writes 1).
- If b = 1, C4 came before B2, so before B3, and final y = 1.
- If b = 2, final y = 2 when C4 takes effect before B3, and 1 when C4 takes effect after B3.

**Final x (Q2)**

The last write to x is A5 (3), B5 (b) or C2 (c).

**Case A3 = 0.** A3 takes effect before B1 and before C4. All of x ∈ {0, 1, 2, 3} and y ∈ {1, 2} are possible:
- x = 3: A5 is last.
- x = 2: B5 is last with b = 2.
- x = 1: B5 is last with b = 1, or C2 is last with C1 having read 1 from A1.
- x = 0: C1 runs before A1 and C2 is last.
- y = 2 with x = 1, using c = 1: order A1, C1, A2–A5, B1, B2, B4, B5, C2, C4, B3. This gives a = 0, b = 2, x = 1, y = 2.
- y = 2 with x = 0 works the same way with C1 placed before A1.
- y = 1 in any of these: let C4 come after B3.

**Case A3 = 2.** A3 reads 2 from B1, or from B3 with b = 2. The same freedom applies, so all 8 combinations are possible:
- x = 1 can come from c = 1.
- It can also come from b = 1: C4 takes effect between A3 and B2, so A3 still reads B1's 2.

**Case A3 = 1.** A3 takes effect after C4, and C4 is after C2. Then C2 is before A5, so C2 cannot be the last write to x. That leaves x ∈ {3, b}:
- x = 3 with y = 1 or y = 2.
- x = 2 (b = 2) with y = 1 or y = 2. For y = 2, A3 reads 1 between C4 and B3.
- x = 1 needs b = 1, which forces y = 1.

BEGIN
0 0 1
0 0 2
0 1 1
0 1 2
0 2 1
0 2 2
0 3 1
0 3 2
1 1 1
1 2 1
1 2 2
1 3 1
1 3 2
2 0 1
2 0 2
2 1 1
2 1 2
2 2 1
2 2 2
2 3 1
2 3 2
END