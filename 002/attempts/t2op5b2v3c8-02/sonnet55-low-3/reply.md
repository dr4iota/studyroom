Every operation takes effect at a single instant, so the possible outcomes are the same as for all sequential interleavings. Thread B's order is fixed: write 1, write 3, B3, B4. Thread A's order is A1, A3, A4. A2 only writes y, so it does not affect x. Let v be the value A1 reads. A4 writes v to x.

**Case v = 3.** A1 runs after B writes 3, so x is 3 from then on, and A4 writes 3 again. The only outcome is (A3, B3, B4) = (3, 3, 3).

**Case v = 1.** A1 runs between B's two writes. A4 then writes 1, either before B writes 3 or after it.
- If A4 comes before B writes 3, B's later write overwrites it. A3 reads 1 and B reads (3, 3).
- If A4 comes after B writes 3, A3 can read 1 (before B's write of 3) or 3 (after it, but before A4).
- With A4 after B's write of 3, (B3, B4) can be (3, 3) if A4 comes after B4, (3, 1) if A4 falls between B3 and B4, or (1, 1) if A4 comes before B3.
- So A3 is 1 or 3, with (B3, B4) in {(3,3), (3,1), (1,1)}.

**Case v = 0.** A1 runs before any write by B. A4 writes 0 somewhere after A1, and A3 comes before A4.
- If A4 comes before B3, then (B3, B4) = (3, 3) or (0, 0).
- If A4 falls between B3 and B4, then (B3, B4) = (3, 0).
- If A4 comes after B4, then (B3, B4) = (3, 3).
- A3 can read 0, 1, or 3, depending on where it falls relative to B's writes.
- When A4 comes before B writes 1, A3 must read 0, and B reads (3, 3).

**Union.**
- A3 = 0 comes only from v = 0, so (B3, B4) is (3,3), (0,0), or (3,0).
- A3 = 1 allows all five pairs: (3,3), (3,1), (1,1), (0,0), (3,0).
- A3 = 3 allows the same five pairs.

BEGIN
0 3 3
0 0 0
0 3 0
1 3 3
1 3 1
1 1 1
1 0 0
1 3 0
3 3 3
3 3 1
3 1 1
3 0 0
3 3 0
END