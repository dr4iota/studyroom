**Key observation: z never changes from 0.**
- z is written only by A5, and A5 writes the value that A3 read from z.
- A3 runs before A5 in thread A, so when A3 reads z, no write to z has taken effect. A3 returns 0.
- So A4 writes 0 to y, and A5 writes 0 to z.

**Writes to y:** A1 writes 3, A4 writes 0, B2 writes 5 and C1 writes 2.

**Order constraints:** A1 comes before A4, and B1 comes before B2, which comes before B4.

- B1 returns the last y write before B1, or 0 if there is none.
- B4 returns the last y write before B4. That is B2 or any y write after B2.
- The final y is the last y write overall. A1 is always followed by A4, so the final y is the value from A4, B2 or C1: 0, 5 or 2.

**Case: final y = 5 (B2 is the last y write).**
- Nothing writes y between B2 and B4, so B4 = 5.
- B1 can see no write (0), A1 (3), C1 (2) or A4 (0).
- Combinations: (0,5,5), (3,5,5), (2,5,5).

**Case: final y = 0 (A4 is the last y write).**
- A4 must come after B2, so B1 cannot have seen A4.
- If B1 = 0 (no write before B1): B4 can be 5, 3 (A1 between B2 and B4), 2 (C1 between B2 and B4) or 0 (A4 before B4).
- If B1 = 3 (A1 before B1): B4 can be 5, 2 or 0.
- If B1 = 2 (C1 before B1): B4 can be 5, 3 or 0.

**Case: final y = 2 (C1 is the last y write).**
- C1 comes after B2, so B1 cannot be 2.
- If B1 = 0 (no write, or A4 before B1): B4 can be 5, 3, 0 or 2.
- If B1 = 3 (A1 before B1): B4 can be 5, 0 or 2.

BEGIN
0 5 5
3 5 5
2 5 5
0 5 0
0 3 0
0 2 0
0 0 0
3 5 0
3 2 0
3 0 0
2 5 0
2 3 0
2 0 0
0 5 2
0 3 2
0 0 2
0 2 2
3 5 2
3 0 2
3 2 2
END