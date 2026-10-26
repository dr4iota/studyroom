**Reasoning**

**1. Final value of x (Q3).**
- C5 ends before Q, and D1 happens after Q, so all of thread C finishes before D1.
- D1 returned 2 from y, so B5 (the only write of 2 to y) takes effect before D1. That puts B1–B5 before D1.
- D1 happens before R. A5 ends after R, so A6 also happens after R.
- So by the time A6 runs, these writes to x have taken effect: C2, C3 (writes 1), B2 (writes 2), B4 (writes 3) and C5.
- A6 returned 0 from x. The last write to x before A6 must therefore have written 0. The only candidate is C5, and only if C1 read y = 0. So C1 took effect before B5, and C5 took effect after B4.
- D3 writes 3 to x. It cannot come before A6, or A6 would return 3. So D3 comes after A6, and nothing writes x after D3.
- Final x = 3.

**2. A2 and A3 (Q1, Q2).**
- A1, A2 and A3 come before P. D5 comes after P. A4 and A5 come after A3.
- So the writes to z that can take effect before A3 are, in order:
  - B1 (writes 3)
  - B3 (writes 2)
  - D2 (writes 3)
- D2 can come before A3. D2 only needs to follow D1, and the D1 → D3 → A6 chain does not stop D2 from preceding A3.
- That gives this sequence of z values: 0 → 3 → 2 → 3.
- A2 sees some point in this sequence, and A3 sees the same point or a later one. A1 returning 0 is consistent with every case.
- The possible (A2, A3) pairs are:
  - A2 = 0: A3 = 0, 3 or 2
  - A2 = 3: A3 = 3 or 2
  - A2 = 2: A3 = 2 or 3

BEGIN
0 0 3
0 3 3
0 2 3
3 3 3
3 2 3
2 2 3
2 3 3
END