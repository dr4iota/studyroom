The possible outcomes are 14 triples, listed between BEGIN and END below.

Key facts behind the enumeration:
- B2 and C2 must read 0, but B1 and C1 write 3 earlier in their own threads. So the last write before each of those reads must be a zero write from A.
- The only possible zero writes are A2 (when A1 reads 0) and A4 (when A3 reads 0). A3 can read 0 only if A2 wrote 0, so A1 must read 0 in every execution.
- Case I (A3 reads 0, so A4 writes 0) gives 7 outcomes.
- Case II (A3 reads 2 or 3, so A4 writes that nonzero value) gives 7 outcomes. The triple (3, 3, 2) is impossible because B3 would have to be the last write yet C4 would have to sit between B3 and B4.

Each listed triple is backed by an explicit interleaving that satisfies all rules.

Asked values: Q1 = A3's read, Q2 = B4's read, Q3 = final x.

BEGIN
0 0 0
0 0 3
0 2 0
0 2 2
0 2 3
0 3 0
0 3 3
2 2 2
2 2 3
2 3 2
2 3 3
3 2 2
3 2 3
3 3 3
END