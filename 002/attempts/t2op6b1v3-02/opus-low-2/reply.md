**Approach.** Each operation takes effect at a single instant, so every execution is an interleaving of A1–A5 and B1–B5 that keeps each thread's order. Thread A writes 2 (A3), then 3 (A4), then 2 (A5). Thread B writes 1 at B3 and again at B5. The reads A1 and A2 do not affect any asked value.

**Possible values of B1.** B1 comes before B3, so B1 can only see A's writes.
- 0 if B1 takes effect before A3.
- 2 if B1 is between A3 and A4, or after A5.
- 3 if B1 is between A4 and A5.

**Possible values of B4.** B4 comes after B3.
- 1 if no A write takes effect between B3 and B4.
- Otherwise it is the value of the last A write in that gap: 2 (from A3 or A5) or 3 (from A4).

**Final value.** The last write is either B5, giving 1, or A5, giving 2.

**Case B1 = 0** (A3, A4 and A5 all come after B1):
- B4 = 1: all of A's writes can come after B5, giving final 2. Or A5 can come before B3, giving final 1.
- B4 = 2: A3 can fall between B3 and B4 with A4 and A5 after B5, giving final 2. Or A5 can fall in that gap, giving final 1.
- B4 = 3: A4 falls between B3 and B4. A5 can come before B5 (final 1) or after it (final 2).

**Case B1 = 2:**
- B1 between A3 and A4:
  - B4 = 1 with final 1: A4 and A5 come after B1 and before B3.
  - B4 = 1 with final 2: order B3, B4, B5, A4, A5.
  - B4 = 2 with final 1: A5 falls between B3 and B4. A5 is then before B5, so the final value can only be 1.
  - B4 = 3 with final 1 or 2: A4 falls between B3 and B4, and A5 comes before or after B5.
- B1 after A5: no A writes remain, so B4 = 1 and the final value is 1.

**Case B1 = 3** (B1 between A4 and A5):
- B4 = 1: A5 can come before B3 (final 1) or after B4. If it is after B4, it can come before B5 (final 1) or after B5 (final 2).
- B4 = 2: A5 falls between B3 and B4, so the final value is 1.
- B4 = 3: impossible, because A4 is already before B1.

BEGIN
0 1 1
0 1 2
0 2 1
0 2 2
0 3 1
0 3 2
2 1 1
2 1 2
2 2 1
2 3 1
2 3 2
3 1 1
3 1 2
3 2 1
END