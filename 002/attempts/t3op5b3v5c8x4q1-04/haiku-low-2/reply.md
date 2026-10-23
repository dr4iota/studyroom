Two final values are possible: 4 and 5.

**Why A4 = 5 forces a specific source.** A2 (writes 3) sits between A1 and A4 in program order, so the last write before A4 must come after A2. A1's value 5 is therefore overwritten before A4 can read it. The only 5-writes that can fall after A2 are C5 (if C4 read 5) or B2 (if B1 read x = 5). B2 is impossible: x = 5 only comes from A5, which runs after A4, and that creates a cycle with B1 < B2 < A4 < A5 < B1. So C5 must write 5 and must occur between A2 and A4.

**Which write can be last.**
- B2 is always followed by B3, so B2 is never last.
- C2 is always followed by C5, so C2 is never last.
- A2 cannot be last, because A4 needs a 5-write after A2.
- A1 cannot be last, because A2 follows it.
- So the last write is B3 (value 4) or C5 (value 5). This rules out 0 and 3.

**Witnessing schedules.**
- Final 4: C2 < A1 < C4 (reads 5) < A2 < C5 (writes 5) < A4 (reads 5), then B1 < B2 < B3 last. A4 reads 5 and B3 writes the final 4.
- Final 5: C2 < A1 < C4 (reads 5) < A2 < B3 < C5 (writes 5) < A4 (reads 5). Here C5 is the last z-write, so the final value is 5.

BEGIN
4
5
END