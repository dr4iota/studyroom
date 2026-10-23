Notation: let a be the value A1 reads and b the value B4 reads. B3 must read 3, so B2 comes before B3.

**Q1 (value of A1).** The writes to x are B1 (1), B2 (3), A2 (2) and A5 (3). A2 and A5 come after A1 in thread A, so A1 can only see 0, 1 or 3. A1 reads 2 never.

**What affects y.** y is written by A3 (value a), B5 (value 2) and B6 (value b). B5 comes before B6. B4 comes before B5, so B4 reads 0 or a, and it reads a only if A3 happened before B4. A4 follows A3 and reads a, 2 (if B5 fell between A3 and A4), or b (if B6 fell between them). The final y is b if B6 is last, or a if A3 comes after B6.

**Case a = 0** (A1 before B1). Every write of A3 and B6 stores 0, and B5's 2 is overwritten by B6, so the final y is 0.
- A4 reads 0 or 2.
- Results: (0,0,0) and (0,2,0).

**Case a = 1** (A1 after B1 and before B2).
- If b = 0 (B4 before A3):
  - A4 can read 1, with final y 1 (B4, B5, B6 all before A3) or final y 0 (B6 after A4).
  - A4 can read 2, with final y 0.
  - A4 can read 0 (B6 between A3 and A4), with final y 0.
  - Results: (1,1,1), (1,1,0), (1,2,0), (1,0,0).
- If b = 1 (A3 before B4), B6 writes 1 last, so the final y is 1.
  - A4 reads 1 or 2.
  - Results: (1,1,1), (1,2,1).

**Case a = 3** (A1 after B2 and before A2). B3 can read 3 before A2, so the same orderings as a = 1 work with 3 in place of 1.
- Results: (3,3,3), (3,3,0), (3,2,0), (3,0,0), (3,2,3).

BEGIN
0 0 0
0 2 0
1 1 1
1 1 0
1 2 0
1 0 0
1 2 1
3 3 3
3 3 0
3 2 0
3 0 0
3 2 3
END