**Key deductions**

- D1 returned 2 ⇒ B5 (write 2 to y) took effect before D1, hence before R.
- A6 (after R) returned 0 ⇒ the last write to x before A6 wrote 0. Only C2/C5 can write 0 (if C1 read 0). D3 (write 3 to x) is after Q and before R, and C2 is before C5‑start which is before Q, so C2 cannot come after D3. Hence C5 writes 0 after D3 (and after B4), and C1 read 0. No write to x can follow, so the **final x = 0**.
- A2 (before P) can see z = 0, 3 (B1 or D2 – D2 can precede A2 since Q need not follow P), or 2 (B3); it cannot see D5 (starts after P).
- A3 (after A2, before A4) can additionally see 1 from D5 (D5 may start after P and take effect before A3). Order constraints on z writes (B1 → B3 → … D2 → … D5) rule out going back to 0 after seeing 3 or 2.

BEGIN
0 0 0
0 1 0
0 2 0
0 3 0
2 1 0
2 2 0
2 3 0
3 1 0
3 2 0
3 3 0
END