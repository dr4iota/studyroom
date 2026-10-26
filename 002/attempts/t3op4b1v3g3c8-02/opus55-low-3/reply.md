**Key constraint.** B2 must return 0 even though B1 wrote 3 just before it. So some write of 0 must take effect between B1 and B2. The same holds for C: a write of 0 is needed between C1 and C2.

Only thread A can write 0:
- A2 writes 0 if A1 read 0.
- A4 writes 0 if A3 read 0.

There are two ways to provide the needed zero writes.

**Case 1: A2 alone serves both B and C.**
- A1 reads 0 before B1 and C1.
- A2 writes 0 after both B1 and C1, but before B2 and C2.
- A3 is then free:
  - **A3 = 0** (before B3 and C3). A4 writes 0 later. The final value can be 0 (A4 last), 2 (B3 last) or 3 (C4 last). B4 can return 0, 2 or 3, except that a final value of 2 forces B4 = 2.
  - **A3 = 2.** A4 writes 2. The final value is 2 or 3. B4 returns 2 or 3.
  - **A3 = 3** (after C4). A4 writes 3. The final value is 3, or 2 if B3 is last. A final value of 2 forces B4 = 2.

**Case 2: A2 and A4 each serve one thread.**
- Example order: A1, B1, A2, B2, A3(=0), C1, A4, C2, followed by the rest.
- This gives A3 = 0, so it adds no new combinations beyond Case 1.

BEGIN
0 0 0
0 2 0
0 3 0
0 2 2
0 0 3
0 2 3
0 3 3
2 2 2
2 3 2
2 2 3
2 3 3
3 2 3
3 3 3
3 2 2
END