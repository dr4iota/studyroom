Every combination is possible except two kinds: A1 = 1 with A2 = 0, and A1 = 1 with B2 = 2. That leaves 14 combinations.

**Timing constraints that follow from the sync rules**
- All of Thread A happens before P.
- B3 ends after P. Its write may take effect before P, because B3's start is not tied to P.
- B4 starts after B3 ends, which is after P. So B4's write always takes effect after all of Thread A and can never affect A1, A2 or A3.
- All of Thread C finishes before Q. The C writes may interleave with Thread A in any way.

**Possible values of each read**
- **B2** reads y after B1 has written 1. It returns 1, or 2 if C2 or C4 took effect in between.
- **A3 = 2** needs the last write to x before A3 to write 2. That is C1, C3, or B3 when B2 = 2.
- **A2** can return 0 (no write to y yet), 1 (from B1) or 2 (from C2 or C4).
- **A1** can return 0, 2, or 1. A1 = 1 is the case that needs care.

**The case A1 = 1**
- B3 must take effect before A1 and write 1, so B2 = 1.
- B1 then comes before A1, so A2 returns 1 or 2, never 0.
- A3 = 2 still works if C3 takes effect after A1 and before A3. Example order: B1, B2 (reads 1), B3, A1 (reads 1), C1, C2, C3, A3.

**The cases A1 = 0 and A1 = 2**
- Each of the 6 pairs of A2 ∈ {0, 1, 2} and B2 ∈ {1, 2} can be arranged.
- For example, take A1 = 0, A2 = 0. Let A1 and A2 run first, then C1 before A3. B1 and B2 happen later, and C2 may come before or after B2, so B2 reads 1 or 2.
- For A1 = 2, C1 is placed before A1, and the rest is arranged the same way.

Values are listed in the order A1, A2, B2.

BEGIN
0 0 1
0 0 2
0 1 1
0 1 2
0 2 1
0 2 2
1 1 1
1 2 1
2 0 1
2 0 2
2 1 1
2 1 2
2 2 1
2 2 2
END