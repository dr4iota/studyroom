Every combination of (A2, A4) that is consistent with the order of writes to y can occur, and the final x can be 0 or 2.

**Final value of x.** The only writes to x are B1 and B3 (both write 2) and A5–A7, which all write the value A1 read.
- A3 returned 2, so B1 took effect before A3. A1 therefore read either 0 (before B1) or 2 (after B1).
- If A1 read 2, A5–A7 write 2, so x ends at 2.
- If A1 read 0, A5–A7 write 0. Then x ends at 0 if B3 takes effect before A7. It ends at 2 if B3 is delayed until after A7.

**Values of A2 and A4.** The writes to y happen in the order B2 (2), B4 (2), B7 (1). So y goes through the values 0, then 2, then 1 over time. A2 comes before A4 in thread A, so the pair (A2, A4) must follow that order:
- (0,0), (0,2), (0,1), (2,2), (2,1), (1,1).

Each pair is achievable. A3 only needs B1 to have happened, so thread B can run freely before or after A2 and A4. For example, A2 = 1 with A1 = 0 works if A1 runs before B1, then B1, B2 and B7 run, then A2 and the rest of A.

Every pair works with each final x, since the choice of A1 and the timing of B3 are independent of y.

BEGIN
0 0 0
0 0 2
0 2 0
0 2 2
0 1 0
0 1 2
2 2 0
2 2 2
2 1 0
2 1 2
1 1 0
1 1 2
END