Q1 is always 0, and the final value of z can be 0, 1 or 5.

**Key observation:** B5 is the only write to z, and it writes the value B4 read from y. So z starts at 0 and is changed at most once, to B4's value.

**Q1 (C3):** C4 comes after C3 in thread C and is known to return 0.
- If B5 writes a nonzero value v and C3 sees it, B5 took effect before C3. Then C4 would also see v, which contradicts C4 returning 0.
- So if B5 writes a nonzero value, C3 must read z before B5 and gets 0.
- If B5 writes 0, C3 gets 0 either way.

Therefore C3 always returns 0.

**Q2 (final z = value read by B4):** B4 comes after B3, which writes 1 to y, so B4 cannot see B1's 2. B4 sees whichever write to y took effect last before it:
- **B3 or C1:** both write 1, so z ends as 1.
- **A4 after A1 read 0:** A4 writes A1's value. A1 can read x before B2 writes 5, so A1 returns 0. Take the order A1, A2, B1, B2, B3, A3, A4, B4, B5.
  - A3 then reads 5 and A2 reads z as 0.
  - Thread C can run C2–C4 before B5, so C4 reads 0.
  - B4 reads 0, so z ends as 0.
- **A4 after A1 read 5:** A1 reads x after B2, so A1 returns 5 and A4 writes 5. Let A4 take effect after B3 and before B4. B5 must come after A2 and C4, which is also possible, so z ends as 5.

BEGIN
0 0
0 1
0 5
END