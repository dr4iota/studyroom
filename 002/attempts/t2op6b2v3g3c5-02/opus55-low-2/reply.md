Every operation takes effect at a single instant, so each execution is one interleaving of the operations, keeping each thread's own order.

**Constraint from the known result.** A2 reads y = 1. Only B1 writes 1 to y, and no other write to y may come between B1 and A2. So B1 takes effect before A2.

**Writes that matter.**
- Writes to x: A1 writes 1, A3 writes 2, and B5 writes v3. Here v3 is the value B3 read.
- Writes to y: B1 writes 1, A4 writes 3, and B4 writes v2. Here v2 is the value B2 read.
- **Final y:** it is v2 if B4 comes after A4, and 3 otherwise.
- **A5:** it reads v3 if B5 falls between A3 and A5, and 2 otherwise.

**Case v3 = 0 (B3 before A1).**
- Then v2 = 0 too, since B2 comes before B3.
- A5 is 2, or 0 if B5 falls between A3 and A5.
- y is 3 or 0.
- All four mixes are possible. For example, the order A4, B4, B5, A5 gives A5 = 0 and y = 0.

**Case v3 = 1 (B3 between A1 and A3).**
- v2 is 0 (B2 before A1) or 1.
- A5 is 2, or 1 if B5 falls between A3 and A5.
- y is 3 or v2, so it can be 3, 0 or 1.
- Every mix is possible, because B4 and B5 can both come after A4 and before A5.

**Case v3 = 2 (B3 after A3).**
- A5 is always 2: whether B5 writes 2 or comes after A5, x is 2 when A5 reads it.
- v2 can be 0, 1 or 2.
- y is 3 or v2, so it can be 3, 0, 1 or 2.

BEGIN
2 0 3
2 0 0
0 0 3
0 0 0
2 1 3
2 1 0
2 1 1
1 1 3
1 1 0
1 1 1
2 2 3
2 2 0
2 2 1
2 2 2
END