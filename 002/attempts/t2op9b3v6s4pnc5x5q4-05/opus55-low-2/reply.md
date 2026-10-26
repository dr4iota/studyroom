**Q1: A8 is 0 or 5.** A7 writes 0 to x. A8 returns 5 only if B1 takes effect after A7, and then B2 = B8 = 5.

**Facts that hold in every execution:**
- **A2 returns 0.** The only writes to z are in thread B, and the first one (B3) comes after P. A2 is before P. So A3 and A7 both write 0 to x.
- **A4 returns 0.** The writes to y are A5 and B5, and both come after A4. B5 is after S, and A6 is before S.
- **B9 always equals B2.** B9 comes after Q, so after A5. B5 comes after S, so A5 takes effect before B5. B5 is therefore the last write to y before B9, and it writes the value read by B2.

**Q2: B2 is 3, 5 or 0.** B2 comes after P, so after A1, and after B1 in its own thread.
- **3:** B1, then A1, then B2, with A3 not yet taken effect.
- **5:** B1 takes effect after A1 and A3 (or after A3 and A7) and is the last write to x before B2.
- **0:** A3 or A7 takes effect after B1 and A1, before B2.

**Q3: B8 is 0 or 5.** B8 comes after Q, so after A3.
- **If B2 = 0:** the only write to x that can fall between B2 and B8 is A7, which writes 0. So B8 = 0.
- **If B2 = 3:** A3 comes after B1, so B8 = 0.
- **If B2 = 5:** B8 = 5 when no 0-write to x falls between B2 and B8. That happens when A3 was before B1 and A7 is after B8, or when B1 came after A7. Otherwise B8 = 0.

**Possible combinations:**
- When A8 = 5, the only result is 5 5 5 5.
- When A8 = 0, the results are 0 0 0 0, 0 3 0 3, 0 5 0 5 and 0 5 5 5.

BEGIN
5 5 5 5
0 0 0 0
0 3 0 3
0 5 0 5
0 5 5 5
END