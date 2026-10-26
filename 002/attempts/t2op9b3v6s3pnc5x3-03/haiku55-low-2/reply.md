Each combination below was checked against an explicit interleaving that satisfies all the sync constraints.

**Constraints:** Thread A's operations before R, P, and Q (A1–A5 before R, A1–A7 before P, A1–A9 before Q) and Thread B's operations after R, Q, and P (B5 after R, B6–B7 after Q, B8–B9 after P) reduce to two real ordering requirements: A5 before B5, and A9 before B6. The sync points can always be placed to satisfy the rest.

**Key facts:**
- **Q1 (A1):** Only B3's write of 3 can precede A1, so Q1 ∈ {0, 3}. Also A1 ≤ A2 in the sense that a 3 seen at A1 is still seen at A2.
- **Q2 (A5):** x is last written by A4 (which copies A2) or by B1 (writes 5). B7 comes after A5, so Q2 ∈ {A2's value, 5}.
- **Q3 (final z):** B9 always comes after A9 and B3, so B9's write of B2's value is the final write to z. B2 reads 0 or 5 (never 3, since B3 is after B2), so Q3 ∈ {0, 5}.

**Joint feasibility:**
- Q3 = 0 requires B2 before A3. This allows (Q1, Q2) = (0,0), (0,3), (0,5), (3,3), (3,5). The pair (3,0) is impossible because A5 cannot read 0 once A2 has read 3.
- Q3 = 5 requires A3 before B2, which forces A1 = A2 = 0 (B3 would come after A2). This allows Q2 = 0 or 5.

BEGIN
0 0 0
0 3 0
0 5 0
3 3 0
3 5 0
0 0 5
0 5 5
END