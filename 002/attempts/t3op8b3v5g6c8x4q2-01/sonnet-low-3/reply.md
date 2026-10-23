Q2 is always 4, and Q1 can be 1 or 5.

**Writes to y.** The writes to y are A1 (1), A4 (4), B4 and B5 (both write what B3 read), and C1 (5).

**Why B4 and B5 always write 4.**
- B2 returns 4, and only A4 can supply that 4 early, since B4 and B5 come after B2. So A4 happens before B2.
- B3 reads after B2. After A4, the only other possible y-writes are C1 (5), A1 (1) and B4/B5.
- B3 cannot read 1, because A1 comes before A4 and nothing writes 1 again.
- B3 cannot read 5. C4 needs a 4-write after C1. B-writes of 4 would need B3 = 4, so that 4 would have to be A4. That would put C1 before A4, which is before B2, so y is already 4 when B3 reads.
- So B3 = 4, and B4 and B5 both write 4.

**Q2 (C6).** C6 comes after C4, and C4 returned 4 after C1. After that point the only y-writes left are 4s. A1 is earlier than A4, and C1 is earlier than C3, which is earlier than C4. So C6 = 4.

**Q1 (A3).** A3 runs between A1 and A4. It cannot read 0, because A1 has written. It cannot read 4, because no 4 is written before A4. So A3 is 1 or 5.

**Both values of A3 are achievable.** Take the order where all of A and all of C finish before B1:
- Either A3 reads y before C1 (A3 = 1), or after C1 and before A4 (A3 = 5).
- C3 reads 5 after C1, and A4 then makes y = 4 for C4 and C6.
- B1 is then the last write to z, so z = 1 at the end.
- Afterwards B2, B3 and B7 read 4 and B4/B5 write 4. B6 reads x = 4 because A2 and C5 both wrote 4.

BEGIN
1 4
5 4
END