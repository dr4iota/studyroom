**Constraints from the sync points**

- B1–B6 happen before R and S, and B7–B8 happen before P and Q.
- All of thread A happens after Q, and A1 is also after R. So every operation of A runs after B8 has finished.
- B9 has no sync constraint. It can take effect at any point while A runs.

**Thread B before A starts**

- When B2 reads y, nothing has written to y yet, so B2 returns 0.
- B4 writes 3 to y. B8 then writes B2's value (0) to y, so y = 0.
- B1 writes 2 to x and B3 writes 4 to x, so x = 4.
- B7 writes 1 to z, so z = 1.
- B9 will later write B2's value (0) to x.

**Thread A**

- A1 reads y and gets 0. A2 writes 0 to z.
- A3, A5, A6 and A8 all read x. Each returns 4 if it takes effect before B9, and 0 if after.
- A4 writes A3's value to y. Nothing writes y after that, so the final y equals A3's value.

**Possible outcomes**

The four reads of x happen in order, so they return 4 up to the point where B9 takes effect and 0 from then on. B9 can fall in any of five places:

| B9 takes effect | A5 | A6 | A8 | final y |
|---|---|---|---|---|
| after A8 (or never during A) | 4 | 4 | 4 | 4 |
| between A6 and A8 | 4 | 4 | 0 | 4 |
| between A5 and A6 | 4 | 0 | 0 | 4 |
| between A3 and A5 | 0 | 0 | 0 | 4 |
| before A3 | 0 | 0 | 0 | 0 |

BEGIN
4 4 4 4
4 4 0 4
4 0 0 4
0 0 0 4
0 0 0 0
END