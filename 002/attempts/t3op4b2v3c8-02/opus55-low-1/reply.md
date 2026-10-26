Every combination below is reachable, and nothing else is: 12 combinations where B2 reads 2, plus 13 more where B2 reads 1, for 25 in total.

There are no sync points, so any interleaving that keeps each thread's own order is allowed.

**Which values can appear**

- **B2 (call its value b).** B2 runs after B1, so it sees either B1's 2 or A1's 1.
  - b = 1 exactly when A1 takes effect between B1 and B2.
  - b = 2 when A1 is before B1 or after B2.
- **Writes to x.** A2 writes 2. B3 and B4 write b. C4 writes the value C1 read, call it c.
- **C1 (c).** C1 reads 0 if it comes before every write to x. Otherwise it reads 2 or 1, depending on which write to x came last.
- **A3.** A3 comes after A2, so it returns 2 unless B3, B4 or C4 takes effect between A2 and A3.
- **C2.** C2 returns 0, 1 or 2, depending on whether it comes before both y-writes or which one came last.
- **Final x.** Final x is whichever of A2, B4 and C4 takes effect last.

**Case b = 2.** Every write to x is 2 or 0, so A3 and the final x are each 0 or 2.

- A3 = 0 needs C1 first (so c = 0) and C4 between A2 and A3.
- Final x = 0 needs C4 last with c = 0.
- C2 can be 0, 1 or 2 in each case:
  - C2 = 0: put C2 before A1 and B1.
  - C2 = 1: put C2 after A1, which is before B1.
  - C2 = 2: put C2 after B1 and keep A1 before B1.

For example, for (0, 2, 0): A1, B1, C1, C2, C3, B2, B3, B4, A2, C4, A3. Here C1 reads 0, C2 reads 2, B2 reads 2, and C4 writes 0 last.

So all 12 combinations of A3 ∈ {0, 2}, C2 ∈ {0, 1, 2} and final x ∈ {0, 2} are possible.

**Case b = 1** (order B1, A1, B2). Here C2 = 0 means C2 is before B1, C2 = 2 means between B1 and A1, and C2 = 1 means after A1. This case adds the combinations that contain a 1:

- **A3 = 1 (B3 between A2 and A3), final 0 or 1.** Final 1 is B4 or C4 last with c = 1. Final 0 is C4 last with c = 0, which needs C1 before A2 and B3. All three C2 values work in both cases. For example, for (1, 0, 0): C1, C2, C3, B1, A1, B2, A2, B3, A3, B4, C4.
- **A3 = 1, final 2.** After A3 only C4 can still write, so C4 must write 2. That means C1 read 2, so C1 is after A2, which is after A1. C2 comes after C1, so C2 = 1 is the only option. Example: B1, A1, B2, A2, C1, B3, A3, B4, C2, C3, C4.
- **A3 = 0, final 1.** C4 writes 0 between A2 and A3, and B4 writes 1 later. All three C2 values work. Example: C1, C2, C3, B1, A1, B2, A2, C4, A3, B3, B4.
- **A3 = 2, final 1.** All of C runs early, then B1, A1, B2, A2, A3, B3, B4. All three C2 values work.

BEGIN
0 0 0
0 1 0
0 2 0
0 0 2
0 1 2
0 2 2
2 0 0
2 1 0
2 2 0
2 0 2
2 1 2
2 2 2
1 0 0
1 1 0
1 2 0
1 0 1
1 1 1
1 2 1
1 1 2
0 0 1
0 1 1
0 2 1
2 0 1
2 1 1
2 2 1
END