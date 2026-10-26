The only possible final values of z are 4 and 5. Each is reachable by an ordering that respects every thread's program order and the known result that A4 reads 5.

**Why A4 reads 5.** A2 writes 3 before A4, so the last write to z before A4 must be a 5 written after A2. The only candidates are B2 and C5. B2 can only write 5 if B1 read 5 from A5, but A5 comes after A4, so B2 is too late. Therefore C5 writes 5, and it sits between A2 and A4.

**Why C4 reads 5.** C5 writes the value C4 read, so C4 read 5. The only 5-writes that could precede C4 are A1 and B2, and B2 is again too late. So A1 is the last z-write before C4, which forces C2 to come before A1 (C2 is earlier than C4 in C's program order) and A2 to come after C4.

**Resulting chain.** This gives C2 < A1 < C4 < A2 < C5 < A4 < A5. B2 and B3 cannot fall between A1 and C4, or between C5 and A4.

**Final z.** If B3 falls before C5, then C5 is the last z-write, so z = 5. If B3 falls after A4, then B3 is the last z-write, so z = 4. B2 can never be the last z-write, because B3 always follows it and overwrites it.

**Both values are achievable:**
- **z = 5:** run all B operations first, then C2, A1, C4, A2, C5, A4, A5. C5 is the final z-write.
- **z = 4:** run C2, A1, C4, A2, C5, A4, then A5, B1 (reads 5), B2 (writes 5), B3 (writes 4). B3 is the final z-write.

BEGIN
4
5
END