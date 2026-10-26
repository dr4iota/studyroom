Reading the sync-point lines literally, "before P" constrains only the steps above a line, so Thread A has no timing constraint relative to P or Q. Thread B's constraints (B3 ends after P, and B4 spans Q) and Thread C's (all of C finishes before Q) can always be satisfied by placing P and Q appropriately, so the only real constraints are the per-thread orders and A3 reading 2.

- B2 reads y. Since B1 (writes 1) precedes it, B2 returns 1 or 2 (2 only if C2 or C4 takes effect between B1 and B2).
- If B2 = 1, B3 and B4 write 1 to x, so A3 can only read 2 if it lands after a C write of 2 to x and before B3. This forces A1 ∈ {0, 2}, and all six (A1, A2) pairs are achievable.
- If B2 = 2, B3 and B4 write 2 to x, so A3 reads 2 whenever any x-write precedes it. A1 ∈ {0, 2}, and all six (A1, A2) pairs are achievable with suitable interleavings.

Each of the 12 combinations below has an explicit interleaving that realizes it.

Values are listed as A1, A2, B2.

BEGIN
0 0 1
0 1 1
0 2 1
2 0 1
2 1 1
2 2 1
0 0 2
0 1 2
0 2 2
2 0 2
2 1 2
2 2 2
END