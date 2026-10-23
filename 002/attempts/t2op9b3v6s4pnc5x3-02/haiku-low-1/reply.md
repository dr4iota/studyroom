**Key constraints**

- Thread A: A1–A3 happen before R; A4 onward happen after P and after S; A7 onward happen after Q.
- Thread B: B1–B4 happen before S; B1–B6 happen before P; B7 onward happen after R; B1–B8 happen before Q.

**Forced values**

- **B5** reads x. Only B3 (writes 4 to x) can precede it, and B3 always precedes B5 in program order, so B5 = 4. Hence B6 writes 4 to z and B8 writes 4 to y.
- **A7** reads y. B8 (writes 4) always precedes Q, which precedes A7. A8 writes 2 but comes after A7. So A7 = 4 always.

**A2 (reads z)**

- Writes to z that can precede A2: B1 (4), B6 (4), B9 (3). A5 (2) comes after A2 in program order.
- B9 comes after B7 in program order, and B7 comes after R, which comes after A2. So B9 always comes after A2, and A2 can't see 3.
- A2 ∈ {0, 4}. Both are achievable.

**A3 (reads x)**

- Only B3 (writes 4) can precede A3. A4 and A6 come after A3 in program order.
- A3 ∈ {0, 4}. Both are achievable.

**Joint combinations**

- (A2=0, A3=0): A1 A2 A3 R B1 B2 B3 B4 S B5 B6 P A4 B7 B8 Q A5 A6 A7 A8 B9
- (A2=4, A3=4): B1 B2 B3 B4 A1 A2 A3 R S B5 B6 P A4 B7 B8 Q A5 A6 A7 A8 B9
- (A2=4, A3=0): B1 A1 A2 A3 R B2 B3 B4 S B5 B6 P A4 B7 B8 Q A5 A6 A7 A8 B9
- (A2=0, A3=4): A1 A2 B1 B2 B3 A3 R B4 S B5 B6 P A4 B7 B8 Q A5 A6 A7 A8 B9

All four combinations are feasible.

BEGIN
0 0 4
0 4 4
4 0 4
4 4 4
END