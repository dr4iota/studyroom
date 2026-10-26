B3 can return 0, 1 or 5, and cannot return 4.

**Writes to y.**
- A1 writes 1.
- B4 writes 4, but it comes after B3 in thread B.
- C5 writes the value C2 read from x. Only C1 and C4 write x, and C4 comes after C2, so C2 can only return 5. C5 therefore writes 5.
- A5 writes whatever A3 read from y.

**Possible values of B3:**
- **0:** B3 runs before any write to y.
- **1:** A1 takes effect, then B3 reads.
- **5:** C1 through C5 complete, then B3 reads. A5 could also write 5 if A3 read it.
- **4 is impossible.** The only writes of 4 to y are B4 and an A5 that copied 4. B4 comes after B3 in thread B. A5 writes 4 only if A3 read 4, which requires B4 to have already taken effect. That would put B4 before B3, contradicting thread B's order.

BEGIN
0
1
5
END