**Reasoning**

- B5 reads y=2 ⇒ C3 wrote 2 ⇒ C2 read 2 ⇒ no B write to x lands between C1 and C2.
- A3=4 and B3=4 ⇒ A1 before B1, and C3 after B3 (so after B1). Write order on y: A1, B1, C3 ⇒ final y = 2.
- A2 precedes A3, which precedes C3, which precedes C5 (the only write to z) ⇒ A2 reads 0.
- x: B2 precedes B3 precedes C3, and C2 precedes C3. B4 is either before C1 (then C4 reads 2, final x = 2) or after C2 (final x = 3, and C4 reads 2 or 3 depending on whether it precedes B4).

BEGIN
0 2 2 2
0 2 3 2
0 3 3 2
END