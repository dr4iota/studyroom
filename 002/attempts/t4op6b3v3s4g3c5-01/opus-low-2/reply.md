Final x is always 3. A2 can return 0, 2 or 3, and A3 can return any value z could hold by then. That gives 11 combinations.

**1. C1 must have read 0.**
- A6 reads x = 0, and A6 comes after A5 ends.
- So A6 is after R, which is after D1, which is after Q, which is after C5 ends.
- C3 wrote 1 to x before C5, so the last write to x before A6 must write 0.
- The only writes that could write 0 are C2 and C5, which write the value C1 read. Since C2 comes before C3, it must be C5.
- So C1 read 0, and C5 is the last write to x before A6.

**2. The final value of x is 3.**
- B5 must take effect before D1, because D1 reads y = 2. So B2 and B4 are before D1.
- B2 and B4 cannot fall between C5 and A6, or A6 would not read 0. So they take effect before C5.
- D3 comes after D1, so it is after C5. It cannot take effect before A6, or A6 would read 3. So D3 is after A6.
- Every other write to x (B2, B4, C2, C3, C5) is before D1, so before D3. D3 is the last write to x, and Q3 = 3 in every execution.

**3. What A2 can read from z.**
- The writes to z are B1 (3), B3 (2), A4 (1), A5 (2), D2 (3) and D5 (1).
- A1 reads 0, so A1 takes effect before every write to z.
- A2 is before P, and D5 is after P, so A2 cannot see D5.
- A4 and A5 come after A2 in thread A, so A2 cannot see them either.
- A2 can see B1, B3 or D2, or none of them. So A2 is 0, 3 or 2.

**4. What A3 can read from z.**
- A3 is before A4 and A5, but nothing forbids D5 from taking effect before A3. So A3 can return 1.
- Any value z held when A2 read it, or a later value, is possible for A3:
  - A2 = 0: A3 can be 0, 1, 2 or 3.
  - A2 = 2 (after B3): A3 can be 2, 3 (D2), or 1 (D5).
  - A2 = 3 (after B1 or D2): A3 can be 3, 2 (B3), or 1 (D5).

BEGIN
0 0 3
0 1 3
0 2 3
0 3 3
2 1 3
2 2 3
2 3 3
3 1 3
3 2 3
3 3 3
END