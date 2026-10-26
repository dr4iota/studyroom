Every combination below is reachable. These are the values each question can take:

- **Final y.** C3 writes 2, but C4 always runs after C3 and overwrites it with the value C2 read. C2 runs before C3, so it can only read 0 or 3 (3 from D1). So y ends as 0 or 3 and never 2.
- **Values in x.** D3 writes what D2 read, which can be 0, 2 or 3. A3 writes what A2 read, which is 0 or whatever D3 wrote. So x only ever holds 0, 2 or 3.
- **2 and 3 together.** The only source of 2 or 3 in x is D3, which writes just one value. So 2 and 3 never both appear in x in the same execution.
- **A1 and B3.** Each can read 0 if it runs before any write. Each can read 2 (or 3) if it runs after D3 wrote that value. A1 and B3 are in different threads, so one can read 0 early while the other reads 2 or 3 late.
- **Allowed pairs (A1, B3).** These are (0,0), (0,2), (2,0), (2,2), (0,3), (3,0) and (3,3). The pairs (2,3) and (3,2) are excluded.
- **Pairing with y.** Each pair works with either final y of 0 or 3:
  - For x = 2, the order C2 (reads 0), D1, C3, D2 (reads 2), D3, C4 gives y = 0. The order D1, C2 (reads 3), C3, D2, C4 gives y = 3.
  - For x = 3, y = 0 or 3 is similarly reachable. When x stays 0, D3 can run late and y can end as 0 or 3.

BEGIN
0 0 0
0 0 3
0 2 0
0 2 3
2 0 0
2 0 3
2 2 0
2 2 3
0 3 0
0 3 3
3 0 0
3 0 3
3 3 0
3 3 3
END