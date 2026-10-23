The approach is to fix what A1 reads (call it a), then check which (B5, C4, final y) triples each case allows.

**Basic facts**
- x is written only by C2, so B2 reads x as 0 or 1. Call that value b. It is what B3 writes to y.
- The writes to z are B1 (1), C1 (2), and A2 and A3 (both a).
- The final y is a or b, whichever of A4 and B3 takes effect later.

**Case a = 0** (A1 takes effect before both B1 and C1)
- **C4 = 1:** B1 must come after C1, with no write of 0 between B1 and C4.
  - Then B5 can only be 1 or 0. B5 = 2 would need C1 after B1.
  - y can be 0 or 1 in both cases.
- **C4 = 2:** B5 can be 0, 1 or 2, and y can be 0 or 1.
- **C4 = 0:** A2 or A3 takes effect between C1 and C4.
  - B5 = 0 or B5 = 1: y can be 0 or 1.
  - B5 = 2: B5 must fall between C1 and A2. Then A4 comes after B5, which is after B3, so y = a = 0 only.

**Case a = 1** (B1 is the later of B1 and C1 before A1)
- B5 and C4 cannot be 0.
- (1,1), (2,2) and (1,2) each allow y = 0 and y = 1.
- (B5 = 2, C4 = 1) needs the order B1, A1, C1, B2–B5, A2, C4. A4 then comes after B3, so y = 1 only.

**Case a = 2** (C1 is the later of B1 and C1 before A1)
- B5 and C4 cannot be 0.
- All four (B5, C4) pairs allow y = 2 (A4 last).
- Each pair also allows y = 0 and y = 1, by placing B3 after A4 and B2 before or after C2.

**Combined combinations (B5, C4, y)**

BEGIN
0 0 0
0 0 1
1 0 0
1 0 1
2 0 0
0 1 0
0 1 1
1 1 0
1 1 1
1 1 2
2 1 0
2 1 1
2 1 2
0 2 0
0 2 1
1 2 0
1 2 1
1 2 2
2 2 0
2 2 1
2 2 2
END