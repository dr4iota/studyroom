All 12 combinations are possible: A3 and B4 can each be 0 or 3, and x can be 0, 1 or 3, independently.

**Which values can occur**
- Only three operations write to y: A1 writes 3, B3 writes what B2 read, and C4 writes what C1 read. y starts at 0, so every read of y returns 0 or 3. That means A3 and B4 are each 0 or 3.
- x is written only by B1 (1) and C3 (what C1 read, so 0 or 3).
  - If C3 takes effect after B1, the final x is C1's value: 0 or 3.
  - If C3 takes effect before B1, the final x is 1.

**Each combination is reachable**

x = 0: C1 reads 0 (before A1), and C3 takes effect after B1.
- A3=3, B4=3: C1(0), C2, B1, C3, C4, B2(0), B3, A1, A2, A3, B4.
- A3=3, B4=0: the same order, but B4 takes effect before A1.
- A3=0, B4=3: C1(0), C2, B1, C3, A1, B2(3), B3, B4, C4 writes 0, A2, A3.
- A3=0, B4=0: C1, C2, B1, B2(0), C3, A1, B3 writes 0, C4 writes 0, A2, A3, B4.

x = 1: use the four schedules above, but move B1 after C3.

x = 3: A1 takes effect before C1, so C1 reads 3. C3 then writes 3 to x after B1.
- A3=3, B4=3: B1, A1, C1(3), C2, C3, C4, B2(3), B3, B4, A2, A3.
- A3=3, B4=0: B1, B2(0), A1, C1(3), C2, C3, B3 writes 0, B4, C4 writes 3, A2, A3.
- A3=0, B4=0: B1, B2(0), A1, C1(3), C2, C3, C4 writes 3, B3 writes 0, A2, A3, B4.
- A3=0, B4=3: B1, B2(0), A1, C1(3), C2, C3, B3 writes 0, A2, A3, C4 writes 3, B4.

BEGIN
0 0 0
0 0 1
0 0 3
0 3 0
0 3 1
0 3 3
3 0 0
3 0 1
3 0 3
3 3 0
3 3 1
3 3 3
END