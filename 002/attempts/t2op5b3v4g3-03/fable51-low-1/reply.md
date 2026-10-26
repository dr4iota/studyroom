All constraints: B5's known result (1) is automatically satisfied since only B4 writes z. A5 sees z = 0 or 1 depending on whether B4 took effect earlier, independently of B's reads of y. B1 and B2 read y before B3, so they see only A's writes (0 → 1 → 3) in a monotonic order, with B2 seeing a value at least as late as B1.

BEGIN
0 0 0
0 0 1
0 0 3
0 1 1
0 1 3
0 3 3
1 0 0
1 0 1
1 0 3
1 1 1
1 1 3
1 3 3
END