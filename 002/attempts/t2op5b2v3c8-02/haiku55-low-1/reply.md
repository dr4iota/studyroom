Thread A's reads and writes to x, together with B1 and B2, determine all outcomes. A2 only writes y, which is not asked, so it doesn't matter.

- **A1** can see 0, 1, or 3. A4 comes after A1 in program order, so A4's value can't reach A1.
- **A3** comes after A1 and before A4. It can see only the B writes, plus the initial 0.
- **A4** writes A1's value v, and it can be placed before B1, between B1 and B2, or after B2, as long as it comes after A3.
- **B3** and **B4** are ordered reads, so B4 never sees an earlier state than B3 did.

Enumerating the write orders (A4 before B1, between, or after B2) and the read positions gives these reachable (A3, B3, B4) triples:

- A3 = 0: B3, B4 ∈ {(0,0),(0,1),(0,3),(1,0),(1,1),(1,3),(3,0),(3,3)}
- A3 = 1: B3, B4 ∈ {(0,0),(0,1),(0,3),(1,0),(1,1),(1,3),(3,0),(3,1),(3,3)}
- A3 = 3: the same nine pairs as A3 = 1

(3,1) is impossible when A3 = 0, because a 1 written after a 3 would have to be A4 writing 1, which forces A1 to have read 1, and then A3 cannot be 0.

That gives 26 combinations.

BEGIN
0 0 0
0 0 1
0 0 3
0 1 0
0 1 1
0 1 3
0 3 0
0 3 3
1 0 0
1 0 1
1 0 3
1 1 0
1 1 1
1 1 3
1 3 0
1 3 1
1 3 3
3 0 0
3 0 1
3 0 3
3 1 0
3 1 1
3 1 3
3 3 0
3 3 1
3 3 3
END