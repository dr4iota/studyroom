**Key deductions**

- C2 reads x = 2, so some write of 2 to x precedes it. The only candidates are C5 (impossible, it's after C2) and A8 — so A7 must read y = 2 and A8 writes 2 to x, before C2.
- C7 reads x = 3 after C5 wrote 2, so a 3-write to x (A2 or B6) lies between C5 and C7. A2 precedes A8 < C2 < C5, so it must be B6: C5 < B6 < C7.
- Hence B7 (after B6) is after C5 > C2 > A8 > A5. B7 writes 3 to y after A5's write of 2, and no other y-write can follow it. **Final y = 3 always.**
- For z: B4 reads 3 forces B3 < C1 < B4; C6 reads 3 after C4 (writes 4) forces B5 or B8 between C4 and C6. Final z is the later of C8 (writes 2) and B8 (writes 3), both orders being feasible:
  - B1 B2 B3 C1 B4 A3 A1 A2 A4 A5 A6 A7 A8 C2 C3 C4 C5 B5 B6 B7 C6 C7 C8 B8 → y=3, z=3
  - same but B8 before C8 → y=3, z=2

BEGIN
3 2
3 3
END