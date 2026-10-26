Every operation takes effect at a distinct instant, so the outcomes come from the possible orderings of the writes and reads that matter: A2, A4, A5, A7 and B4 through B7. The x-operations are irrelevant to the asked values. A1 must read 0, because the only writes to x come after A1 and copy its value, so every x write is 0.

Two facts constrain the y-operations:
- A2 reads 2, and only B4 (or a B7 that copies a 2) writes 2. So B4 takes effect before A2, and no write that changes y lands between them.
- B5 reads 2, 3, or 0, depending on whether it falls after B4 and before A4, between A4 and A5, or after A5.

Splitting on B5's value gives:
- **B5 reads 2** (B5 before A4): B6 can read 2, 3, or 0; A7 can read 0 or 2; the final y is 0 or 2.
- **B5 reads 0** (B5 after A5): all of B6, A7 and the final y are 0.
- **B5 reads 3** (B5 between A4 and A5): B6 can read 3 or 0; A7 can read 0 or 3; the final y is 0 or 3.

Merging the cases gives 13 distinct combinations.

BEGIN
0 2 0
2 2 2
0 2 2
0 3 0
2 3 2
0 3 2
2 0 2
0 0 2
0 0 0
3 3 3
0 3 3
3 0 3
0 0 3
END