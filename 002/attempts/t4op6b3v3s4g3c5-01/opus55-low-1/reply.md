**Answer:** there are 7 possible combinations. Q3 (the final value of x) is always 3. Q1 and Q2 can be any of seven pairs.

**1. Forced facts from A6 reading x = 0**

- Thread C's chain gives C5 ends < Q < D1 < R < A5 ends < A6. So C5 takes effect before A6.
- C3 (write 1 to x) comes before C5 in thread C, so it also takes effect before A6.
- A6 returns 0, so the last write to x before A6 must write 0. The only write that can be 0 is C5, which writes C1's value. So C1 returned 0.
- C5 must be the last x-write before A6:
  - D1 reads y = 2, so B5 takes effect before D1. B2 and B4 come before B5 in thread B, so both are before A6. They must therefore be before C5 too.
  - D3 comes after D1, which is after Q, so D3 is after C5. It must also take effect after A6, otherwise A6 would read 3.

**2. Final value of x (Q3)**

D3 (write 3 to x) is the last write to x. So the final value of x is 3.

**3. Values of A2 and A3 (Q1, Q2)**

- A2 and A3 come after A1 read z = 0, so no z-write has taken effect before A1.
- Before A3, the only z-writes that can take effect are B1 (3), B3 (2) and D2 (3).
  - A4, A5 and D5 come later: A4 and A5 follow A3 in thread A, and D5 starts after P, which is after A3.
  - D2 can come early. It needs only D1 before it, and D1 needs only Q and B5. Neither has to come after A2 or A3.
- B1 always precedes B3, and D2 can go anywhere among them. So the order of values z holds is either 0, 3, 2, 3 or 0, 3, 3, 2.
- A2 reads some point in that order, and A3 reads the same point or a later one. This gives the pairs:
  - From 0, 3, 2, 3: (0,0), (0,3), (0,2), (3,3), (3,2), (2,2), (2,3).
  - From 0, 3, 3, 2: (0,0), (0,3), (0,2), (3,3), (3,2), (2,2).
- Combined, that is seven pairs, each with final x = 3.

BEGIN
0 0 3
0 3 3
0 2 3
3 3 3
3 2 3
2 2 3
2 3 3
END