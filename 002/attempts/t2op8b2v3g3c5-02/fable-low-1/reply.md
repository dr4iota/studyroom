**Key deductions:**
- x is only ever written by A3/A6, which write A1's value; A1 can only return 0, so x stays 0 and A5 writes 0 to y.
- A2 returned 2 ⇒ B4 (write 2) took effect before A2, so the order of y-writes after that point is A4 (3) then A5 (0), with B7 (writing B5's value) placed anywhere after B5/B6.
- B5 ∈ {2, 3, 0}; B6 must see the same or a later value in the sequence 2 → 3 → 0; B7 writes B5's value.
- A7 returns B7's value if B7 lands between A5 and A7, else 0. Final y is B7's value if B7 is after A5, else 0.

BEGIN
0 2 0
0 3 0
0 0 0
2 2 2
2 3 2
2 0 2
0 2 2
0 3 2
0 0 2
3 3 3
3 0 3
0 3 3
0 0 3
END