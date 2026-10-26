**Reasoning:** x evolves through B's writes 0→3→2→1→2, with A's write 2 (A4) inserted somewhere. A2 and A3 see states in order; A5 comes after A4.

- A4 before B1: A2=A3=0, A5 ∈ {1,2,3}.
- A4 between B1/B2: (A2,A3) ∈ {(0,0),(0,3),(3,3)}, A5 ∈ {1,2}.
- A4 between B2/B3: adds (0,2),(3,2),(2,2), A5 ∈ {1,2}.
- A4 between B3/B4: adds (0,1),(3,1),(2,1),(1,1), A5 = 2.
- A4 after B4: adds (1,2), A5 = 2.

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
0 1 2
3 1 2
2 1 2
1 1 2
1 2 2
END