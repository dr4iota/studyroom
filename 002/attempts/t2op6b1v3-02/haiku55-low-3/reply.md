Each thread's operations take effect in order, and the two threads' effects can interleave in any order. I encoded each interleaving by how many A-operations have taken effect before each B-operation. Then I checked which combinations of (B1, B4, final x) are reachable.

- **B1** sees the last A-write before it: 0 if A has done at most A2, 2 after A3, 3 after A4, and 2 after A5. B-writes can't precede B1, so B1 ∈ {0, 2, 3}.
- **B4** sees B3's write (1) unless an A-write took effect between B3 and B4. The last such write sets the value: A3 gives 2, A4 gives 3, A5 gives 2. So B4 ∈ {1, 2, 3}.
- **Final x** is 1 if B5 takes effect after all of A's operations, and 2 otherwise, since A5 is the last A-write.

Checking the constraints, 14 combinations are reachable. For example, (0, 1, 2) occurs when all of B1 through B4 run before any A-operation and A1 through A5 run after B4 and before B5. The combination (2, 2, 2) is not reachable, because getting B4 = 2 with B1 = 2 forces B4 to come after A5, which makes B5 come last and the final value 1.

BEGIN
0 1 1
0 1 2
0 2 1
0 2 2
0 3 1
0 3 2
2 1 1
2 1 2
2 2 1
2 3 1
2 3 2
3 1 1
3 1 2
3 2 1
END