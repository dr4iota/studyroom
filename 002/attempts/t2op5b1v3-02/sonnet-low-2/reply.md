Only the order of writes to x matters, since A1 is a read whose value isn't asked about.

**Setup.** The B writes take effect in the order 3, 2, 1, 2, so x passes through the states s0..s4 = 0, 3, 2, 1, 2. A4 (write 2) takes effect after A3 and before A5. A2 and A3 read states s_i and s_j with i ≤ j, because reads only see later states as time passes.

**A5.** Let k be the B-state when A4 takes effect (k ≥ j), and m the B-state when A5 takes effect (m ≥ k).
- If no B write falls between A4 and A5 (m = k), A5 reads 2.
- Otherwise A5 reads s_m, for some m > k ≥ j.

So for a given j, A5 can be 2, or s_m for any m > j.

**Cases by j (the state A3 reads):**
- j=0: A3 = 0, A2 = 0, A5 ∈ {1, 2, 3}.
- j=1: A3 = 3, A2 ∈ {0, 3}, A5 ∈ {1, 2}.
- j=2: A3 = 2, A2 ∈ {0, 3, 2}, A5 ∈ {1, 2}.
- j=3: A3 = 1, A2 ∈ {0, 3, 2, 1}, A5 = 2.
- j=4: A3 = 2, A2 ∈ {0, 3, 2, 1}, A5 = 2.

BEGIN
0 0 1
0 0 2
0 0 3
0 3 1
0 3 2
3 3 1
3 3 2
0 2 1
0 2 2
3 2 1
3 2 2
2 2 1
2 2 2
1 2 2
0 1 2
3 1 2
2 1 2
1 1 2
END