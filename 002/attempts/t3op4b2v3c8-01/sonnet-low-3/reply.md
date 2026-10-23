Each triple below is written as A1, B3, C1.

Only B2 and C4 write to y, so which values y can hold decides what each read can return.

**C1.** C1 comes before C4 in thread C, and A never writes y. So the only write that can precede C1 is B2, which gives C1 ∈ {0, 2}.

**B3.** B3 comes after B2 and returns the last write to y at that moment.
- It returns 2 if B2 is the last write, or if C4 wrote 2.
- It returns 3 if C4 wrote 3. This happens when C3 read x = 3 after B1.
- It returns 0 if C4 wrote 0 after B2. This needs C3 to read x = 0, either before B1, or after A3 wrote 0 to x.

So B3 ∈ {0, 2, 3}.

**A1.** A1 can read 0 or 2 directly. It can read 3 only after C4 has written 3.

**B3 = 2.** A1 = 3 needs C4 to write 3 after B3 has read. All A1 ∈ {0, 2, 3} and C1 ∈ {0, 2} combinations are achievable. That gives 6 triples.

**B3 = 3.** C4 writes 3 after B2, and A1 ∈ {0, 2, 3} and C1 ∈ {0, 2} are all achievable. That gives 6 triples.

**B3 = 0.** C4 must write 0 after B2, and that is the only C4 write to y. So y is never 3, which rules out A1 = 3. The remaining pairs are:
- A1 = 0, C1 = 0 works.
- A1 = 2, C1 = 0 works: C1 and C3 happen before B1 and B2, so C3 reads x = 0, and A1 reads 2 after B2.
- A1 = 0, C1 = 2 works: A reads 0 twice before B2, and A3 writes 0 to x after B1. C1 reads 2 after B2, C3 reads x = 0, and C4 writes 0 to y.
- A1 = 2, C1 = 2 is impossible. For C4 to write 0, C3 must read x = 0. With C1 = 2, B1 has already written 3, so something must write 0 to x afterwards, and only A3 can. A3 writes 0 only if A2 read 0, but A1 = 2 means y was already 2 and never returns to 0 before C4 writes it, so A2 cannot read 0.

That gives 3 triples.

BEGIN
0 0 0
2 0 0
0 0 2
0 2 0
0 2 2
2 2 0
2 2 2
3 2 0
3 2 2
0 3 0
0 3 2
2 3 0
2 3 2
3 3 0
3 3 2
END