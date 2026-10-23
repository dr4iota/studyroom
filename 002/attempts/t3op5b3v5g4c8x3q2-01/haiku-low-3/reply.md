**Key observations**

- **A1 always reads 0.** The only write to y is A2, which comes after A1 in thread A's order. So A2 writes 0 to y, and A4 writes 0 to x.
- **x gets two writes:** B1 writes 1, and A4 writes 0. Q2 (final x) is whichever of these takes effect later.
- **C2 must see a 3.** C1 writes 5 and precedes C2, so the last write to z before C2 must be a 3-write (B2 or B4). That means C1 < B_k < C2 for some B_k ∈ {B2, B4}, and A5 (which writes 2) cannot fall between B_k and C2.
- **B1 always precedes C4.** B1 comes before B2, and B2 or B4 must precede C2, which precedes C4. So B1 is always before C4.

**Q1 (C4's read of x)** sees the later of B1 and A4 if A4 is before C4. Otherwise it sees 1 (from B1). It is 0 only if neither has taken effect.

**Possible outcomes**

- **Q1 = 1, Q2 = 1:** A4 takes effect before B1, and both are before C4. Example: C1, B2, A1–A4, B1, C2, C3, C4, A5.
- **Q1 = 0, Q2 = 0:** B1 takes effect, then A4, both before C4. Example: C1, B2, B1, A1–A4, C2, C3, C4, A5.
- **Q1 = 1, Q2 = 0:** B1 is before C4, and A4 is after C4 so A4 is the last x write. Example: C1, B1, B2, C2, C3, C4, A1–A5.
- **Q1 = 0, Q2 = 1 is impossible:** it would need A4 before C4 with B1 after C4, but B1 always precedes C4.

BEGIN
0 0
1 0
1 1
END