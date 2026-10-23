Each thread's operations take effect in listed order, and no sync points constrain the threads, so any interleaving of the two effect sequences is possible. B's writes take effect as 3, 2, 1, 2, and A's reads and write take effect in order R1, R2, R3, W(2), R5.

Let v_0..v_4 = 0, 3, 2, 1, 2 be the value after the first k B-writes. If A2 comes after j B-writes, A3 after k, A4 after m, and A5 after n, then 0 ≤ j ≤ k ≤ m ≤ n ≤ 4. Then A2 = v_j and A3 = v_k. A5 is 2 if n = m (A4's write is the last write), and v_n if n > m.

- A5 = 3 requires n = 1, m = 0, so k = j = 0: (0, 0, 3).
- A5 = 1 requires n = 3 with m ≤ 2, so k ≤ 2: (A2, A3) ∈ {(0,0), (0,3), (3,3), (0,2), (3,2), (2,2)}.
- A5 = 2 is reachable for any k (take m = n ≥ k): (A2, A3) ∈ {(0,0), (0,3), (3,3), (0,2), (3,2), (2,2), (0,1), (3,1), (2,1), (1,1), (1,2)}.

BEGIN
0 0 1
0 3 1
3 3 1
0 2 1
3 2 1
2 2 1
0 0 2
0 3 2
3 3 2
0 2 2
3 2 2
2 2 2
0 1 2
3 1 2
2 1 2
1 1 2
1 2 2
0 0 3
END