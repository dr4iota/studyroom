**Facts that follow from the sync points**

- Thread A runs only after Q, R and S. Q comes after B1–B8 have finished, so B1–B8 all take effect before A1.
- B2 reads y before either write to y (B4 and B8). So B2 returns 0.
- That means B8 writes 0 to y and B9 writes 0 to x.
- B9 has no ordering constraint against thread A. It can take effect at any point relative to A's operations.

**State when thread A starts**

- x = 4 (from B3).
- y = 0 (from B8).
- z = 1 (from B7).

**Thread A's steps**

- A1 reads y and gets 0, because A4 has not happened yet. A2 then writes 0 to z.
- A3 reads x and gets 4 if B9 has not taken effect yet, otherwise 0.
- A4 writes the A3 value to y. This is the last write to y, so the final value of y equals the value A3 read.
- A5, A6 and A8 each read x. x is 4 until B9 takes effect and 0 afterwards. So the reads A3, A5, A6, A8 are a run of 4s followed by a run of 0s.

**Possible outcomes (A5, A6, A8, final y)**

- If A3 read 4 (final y = 4), B9 can fall before A5, between A5 and A6, between A6 and A8, or after A8. This gives four combinations.
- If A3 read 0 (final y = 0), B9 was before A3, so A5, A6 and A8 all read 0.

BEGIN
4 4 4 4
4 4 0 4
4 0 0 4
0 0 0 4
0 0 0 0
END