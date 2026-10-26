Every operation takes effect at a single instant and each thread's operations keep their program order. So every outcome comes from an interleaving of the operations.

**Sources of values.** The writes are B1=2, C1=2, C2=3, C3=2, C4=1, A3 (writes A1's value) and B4 (writes B2's value). A1 is a read, so it can return 0, 1, 2 or 3.

**Q1: B2.** B2 comes after B1, but A3 can overwrite B1's value.
- B2 = 0: A1 reads 0, then B1 writes 2, then A2 reads 2, then A3 writes 0, then B2 reads 0. C1–C4 then run, so C4 supplies the 1 that B3 reads. This works.
- B2 = 1: this happens after C4 completes. Both B2 and B3 read 1 (B3 returned 1), and A2 has already read 2 from B1 or C1.
- B2 = 2: this happens after B1, C1 or C3.
- B2 = 3: this happens between C2 and C3.

**Q2: final x.**
- When B2 = 0, B3 must read 1 and A3 must have run before B2. The 1 can only come from C4, because A3 writes 0 here. So all of C is done before B3, and B4 (writing 0) comes after B3. B4 is therefore the last write of anything, and the final value is 0. Only (0, 0) is possible.
- When B2 is 1, 2 or 3, B4 writes that same value and A3 can run after it. A3 writes A1's value, which can be 0, 1, 2 or 3. A1 can read 3 if it runs between C2 and C3. A2 still reads 2 afterwards, from B1 or C3. So any final value 0–3 is reachable. The final value 1 is also reachable with C4 last.

BEGIN
0 0
1 0
1 1
1 2
1 3
2 0
2 1
2 2
2 3
3 0
3 1
3 2
3 3
END