Only the operations on z matter, since x and y are never read for any asked value. The possible outcomes come from interleaving the z operations of A and B in program order.

**Q3, final z.** The last write to z is either A5 (value 2) or B5 (value 1). Both can come last, so the final value is 1 or 2.

**Q1, A1.** A1 runs before all of A's writes, so it can only see B's writes or the initial 0.
- It returns 0 if it runs before B1.
- It returns 3 if it runs after B1 but before B3.
- It returns 2 if it runs after B3 but before B5.
- It returns 1 if all of B has finished, including B5.

**Q2, B4.** B4 runs after B3, so it never returns 0. It returns the last write before it:
- It returns 2 if no A write falls between B3 and B4.
- It returns 3 if A3 falls between them and A4 does not.
- It returns 4 if A3 and A4 both fall between them and A5 does not.

It also never returns 1, because B5 comes after B4, and A never writes 1.

**Combinations.**
- **A1 = 1.** All of B, including B4, finished before A1, so no A write came before B4. Then B4 = 2. A5 is the last write, so the final value is 2. This gives only (1, 2, 2).
- **A1 = 0, 3 or 2.** A1 only has to precede A3, so B4 can be 2, 3 or 4. For each B4 value, either A5 or B5 can be placed last. For example, with B4 = 3, A3 goes between B3 and B4, and A4 and A5 go after B4. A5 can then come before or after B5. This gives all 6 combinations (B4 ∈ {2, 3, 4}, final ∈ {1, 2}) for each of these three A1 values.

BEGIN
0 2 1
0 2 2
0 3 1
0 3 2
0 4 1
0 4 2
1 2 2
2 2 1
2 2 2
2 3 1
2 3 2
2 4 1
2 4 2
3 2 1
3 2 2
3 3 1
3 3 2
3 4 1
3 4 2
END