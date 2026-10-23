Every operation takes effect at one instant, so each thread's effects follow its program order. The possible outcomes are therefore the interleavings of the five-step sequences that agree with the known results.

**Q3 (C4, read y).** The only writes to y are B5 (value 2) and C5 (value 1). C5 comes after C4 in thread C, so C4 cannot see 1. C4 returns 0 if it runs before B5, or 2 if it runs after. Both are possible, since B5 is last in thread B and nothing forces it before or after C4.

**Q1 (A1, read x).** The writes to x are 2, 3, 2, 2 and A5's write. A5 comes after A1, so it cannot affect A1. A1 returns 0, 2 or 3. A3 must still read 2, which can come from C1, B2 or B4 after A1.

**Q2 (C2, read x).** C1 writes 2 immediately before C2. C2 can therefore return:
- 2, if nothing intervenes.
- 3, if B3 falls between C1 and C2.
- A1's value, if A5 falls between C1 and C2. A5 comes after A3, which has read 2, so this is possible. This gives 0 only when A1 returned 0.

**Combinations:**
- **A1 = 0:** C2 can be 0, 2 or 3 and C4 can be 0 or 2, giving 6 combinations. For C2 = 0, the order is A1, C1, B2 (or just C1), A3 reads 2, A5 writes 0, then C2. The remaining writes can then follow, either before or after C4.
- **A1 = 2:** A5 writes 2 and no write of 0 ever happens, so C2 is 2 or 3. With C4 being 0 or 2, this gives 4 combinations.
- **A1 = 3:** B3 must come before A1, and A3 then reads 2 from a later write by B4 or C1. C2 is 2 or 3. With C4 being 0 or 2, this gives 4 combinations.

BEGIN
0 0 0
0 0 2
0 2 0
0 2 2
0 3 0
0 3 2
2 2 0
2 2 2
2 3 0
2 3 2
3 2 0
3 2 2
3 3 0
3 3 2
END