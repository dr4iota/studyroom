Every outcome below comes from case analysis on the value A1 reads and the interleavings of the y writes.

**Q1 (A1).** Only the writes 1 (B1) and 3 (B2) can precede A1, because A2 comes after A1 and is the only write of 2. So A1 returns 0, 1 or 3. Call that value a.

**Reads and writes of y.**
- B4 returns b. B5 comes after B4, so the only write to y that can precede B4 is A3 (value a). Hence b is 0 or a.
- B6 writes b after B5, so the last write to y is either A3 (value a) or B6 (value b). The final y is therefore never 2.
- A4 comes after A3, so it reads a, 2 (if B5 landed after A3), or b (if B6 landed after A3).

**Case a = 0.** A1 comes before B1, and A3 writes 0, so b = 0 and the final y is always 0. A4 can read 0, or 2 if B5 falls between A3 and A4. The 2 is achievable with the order A1, B1, B2, B3, B4, B5, A2, A3, A4. This gives (0,0,0) and (0,2,0).

**Case a = 1 (A1 falls between B1 and B2) and case a = 3 (A1 falls after B2).** Both cases have the same structure, with v standing for a.
- A4 = v: A3 and A4 run before B5. If B4 ran before A3, b = 0 and the final y is 0. If B4 ran after A3, b = v and the final y is v.
- A4 = 2: B5 falls between A3 and A4. Then b = 0 (B4 before A3) gives final 0, and b = v gives final v.
- A4 = 0: B6 writes b = 0 before A4, and the final y is 0.

Each of these orders is compatible with B3 returning 3: for a = 1, A2 can precede B2 or B3 can precede A2, and for a = 3, B3 can run before A2. This gives (v,v,0), (v,v,v), (v,2,0), (v,2,v) and (v,0,0) for v = 1 and v = 3.

BEGIN
0 0 0
0 2 0
1 1 0
1 1 1
1 2 0
1 2 1
1 0 0
3 3 0
3 3 3
3 2 0
3 2 3
3 0 0
END