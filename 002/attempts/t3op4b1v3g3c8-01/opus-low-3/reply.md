**Approach.** The final value of x comes from whichever write takes effect last among A3, B4 and C4. C1–C3 always come before C4, and B1 always comes before B4.

**Key constraint: B3 returns 1.** The write B3 reads must write 1. That is either C4, or A3 when A1 read 1. B4 comes after B3, so it can't be the source.

**C4 can never be the last write.** If C4 were last, B3 would have to read 1 from A3. That needs A1 to have read 1, which needs C4 to come before A1, and so before A3. C4 would then not be last. So the final value is always the value written by B4 or by A3.

**B2 can only return 1, 2 or 3.** B2 comes after B1, so it never sees the initial 0.

**Case B2 = 3** (B2 reads C2)
- Final 3 (B4 last): B1, C1, C2, B2=3, C3, C4, B3=1, B4. A's steps fit earlier.
- Final 0 (A3 last, A1 read 0): A1=0, C1, A2=2, B1, C2, B2=3, C3, C4, B3=1, B4, A3.
- Final 2: same as above, but A1 reads 2 from C1.
- Final 3 (A3 last, A1 read 3): B1, C2, A1=3, B2=3, C3, A2=2, C4, B3=1, B4, A3.
- A1 = 1 is impossible here. It needs C4 before A1, then B1 after C4 so A2 can read 2. But B2 must read 3 from C2, which comes before C4.
- Finals: 0, 2, 3.

**Case B2 = 2**
- Final 2 (B4 last): works. If A1 read 1, A3 writes 1 before B3 and B4 comes last.
- Final 0 (A3 last): A1=0, then B1, A2=2, B2=2, C1–C4, B3=1, B4, A3.
- Final 2 (A3 last): same pattern with A1 reading 2.
- Final 3 (A3 last): C1, C2, A1=3, C3, A2=2, B1, B2=2, C4, B3=1, B4, A3.
- Finals: 0, 2, 3.

**Case B2 = 1** (B2 reads C4)
- Final 1 (B4 last): works.
- Final 0 (A3 last): A1=0, B1, C1, A2=2, C2, C3, C4, B2=1, B3=1, B4, A3.
- Finals 2 and 3 (A3 last): similar, with A1 reading 2 from C1 or 3 from C2, and A2 reading C3.
- Final 1 also arises with A3 last when A1 read 1.
- Finals: 0, 1, 2, 3.

BEGIN
1 0
1 1
1 2
1 3
2 0
2 2
2 3
3 0
3 2
3 3
END