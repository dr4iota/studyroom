**Reasoning:**

- B4 returned 2, so the last y-write before B4 was a 2. B3 (y=4) precedes B4, so a write of 2 (C2, or A2 writing 2) lands between B3 and B4.
- C3 returned 2, so A4 or A5 wrote 2 to z, meaning A3 read 2 from y, so a 2-write to y preceded A3 with no later write in between.
- Could A2 ever write a non-2 value that C4 sees? If A2 wrote 0 or 4 after C2, then A3 (after A2) would read that value, not 2 — contradiction. So any A2 that lands after C2 must write 2 (A1 read 2).
- C4 comes after C3, which is after A4, which is after A3, which is after the 2-write. All writes of 4 to y (B3) occur before the decisive 2-write (since B4 must see 2 after B3), and A2 can only contribute another 2. So the last y-write before C4 is always 2.

BEGIN
2
END