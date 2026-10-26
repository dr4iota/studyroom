**Approach.** There are no sync points, so every interleaving that respects each thread's own order is allowed. Each read returns the latest earlier write to that block.

**Step 1: What value can y hold?**
- y is only written by B4, which writes whatever B3 read from z.
- B3 runs after B2 (which writes 4 to z). So B3 returns 4, unless C1 (which writes 2 to z) takes effect between B2 and B3, in which case it returns 2.
- Call B4's value v. Then v is 4 or 2, and every read of y returns either 0 (before B4) or v (after B4).

**Step 2: Limits on A3 and C3.**
- A3 and C3 each return 0 or v.
- A2 comes before A3. So if A3 returns 0, A2 also returned 0. If A3 returns v, A2 returned 0 or v.

**Step 3: Which write to x is last?**
The writes to x are B1 (3), C2 (2), A4 (A2's value) and C4 (C3's value). C2 always precedes C4, so C2 cannot be last. That leaves three cases.

- **B1 is last.** B1 must follow C4, which follows C3, and must precede B4, so C3 returns 0. B1 must also follow A4, so A1 to A4 all run before B4, so A3 returns 0. This gives (0, 0, 3).
- **C4 is last.** Final x equals C3's value. Any mix of A3 and C3 in {0, v} can be arranged. This gives (0,0,0), (0,v,v), (v,0,0), (v,v,v).
- **A4 is last.** Final x equals A2's value.
  - If A3 returns 0, then A2 returned 0 and C3 can be either value. This gives (0,0,0), (0,v,0).
  - If A3 returns v, then A2 is 0 or v and C3 is either value. This gives (v,0,0), (v,v,0), (v,0,v), (v,v,v).

**Step 4: Combine.**
Both v = 4 and v = 2 are possible. For v = 2, C1 runs between B2 and B3, which conflicts with nothing else. Substituting both values of v and removing duplicates gives the list below.

BEGIN
0 0 3
0 0 0
0 4 4
4 0 0
4 4 4
0 4 0
4 4 0
4 0 4
0 2 2
2 0 0
2 2 2
0 2 0
2 2 0
2 0 2
END