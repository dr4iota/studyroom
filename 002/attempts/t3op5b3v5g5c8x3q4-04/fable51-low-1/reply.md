**Analysis**

- B4 must return 0. If B2 returned a nonzero value (5 or 1 written by A3), B3 would write that value back, and then nothing could restore x to 0 before B4 — contradiction. So **B2 = 0** always.
- A4 can read 0 (all z‑writes after A4), 5 (B1 or C2 last), or 1 (C3 last).
- If A4 = 1, then C3 (and hence C1) took effect before A4, so A5 (write 3) comes after C1 → final y = 3 only. Otherwise both 3 and 4 are possible.

BEGIN
0 0 3
0 0 4
5 0 3
5 0 4
1 0 3
END