All three asked values vary independently except that A2 (read after A1 in the same thread) cannot see an older value of y than A1 did (y goes 0 → 1 → 2 → 2).

- A1 ∈ {0, 1, 2}, A2 ∈ {0, 1, 2} with A2 ≥ A1.
- B2 ∈ {0, 1} (before or after C3/A5 write 1 to x), independent of the others.

BEGIN
0 0 0
0 0 1
0 1 0
0 1 1
0 2 0
0 2 1
1 1 0
1 1 1
1 2 0
1 2 1
2 2 0
2 2 1
END