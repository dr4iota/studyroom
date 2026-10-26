Every outcome is a combination of three independent choices: which write reaches z first, whether B2 sees A8's write, and whether A2 lands before or after B7.

**Ordering constraints.** B1 ends before P, and A2 starts after P, so B1 precedes A2. A1 ends before S, but A1 also precedes A2 because A2 follows A1 in thread A. A9 starts after Q and ends before R, and B8 starts after R, so all of A finishes before B8. B5 starts after S, so B5–B7 come after B3 and B4.

**The value in z that A4 reads.**
- Only A1 (6) and B1 (1) can write z before A4, and both precede A2. A6, A9 and B8 all come after A4.
- So A4 returns v, where v is 6 or 1, depending on which of A1 and B1 took effect last.
- A6 writes v to z, and A7 reads v. The only other writes to z before A7 are A9's, which also write v.
- A8 is the only write to y, so the final y is v, giving Q3 ∈ {6, 1}.

**B2, B8, B9 and the final z.**
- B2 reads y, which is either 0 or v. It reads v only if A8 took effect before B2. That is possible because B2 only needs to end before Q.
- Call B2's value b. B8 writes b to z, and every other write to z has already happened by then. B9 reads that value, so Q1 = b and the final z is also b.

**Final x.**
- B7 always writes 4 last among B's writes to x.
- A2 writes 1. Either A2 comes before B7, so x ends as 4, or A2 comes after B7, so x ends as 1.
- If A2 comes after B7, then B2 precedes B7, which precedes A2, which precedes A8. B2 therefore reads 0, so b = 0 in that case.

**Combinations.**
- x = 4: v ∈ {6, 1} and b ∈ {0, v}, giving (b, v) = (0, 6), (6, 6), (0, 1), (1, 1).
- x = 1: b = 0 and v ∈ {6, 1}.

BEGIN
0 1 1 0
0 1 6 0
0 4 1 0
0 4 6 0
1 4 1 1
6 4 6 6
END