Each thread's operations take effect in listed order, so A1 < A2 < A3 and B1 < B2 < B3. The writes are A1 (writes 1), B2 (writes 3), and B3 (writes 2). Since B1 comes before both B2 and B3, B1 can only see A1's write (returns 1) or nothing (returns 0).

A2 and A3 see the last B-write that has taken effect before them. Let the B-progress at a read be: none (value 1), only B2 done (value 3), or B3 done (value 2). Progress never decreases over time, and A3 happens after A2, so A3's progress is at least A2's. That gives six possible (A2, A3) pairs:

- (1, 1), (1, 3), (1, 2), (3, 3), (3, 2), (2, 2)

Each pair can occur with B1 returning either 0 (B1 before A1) or 1 (A1 before B1, and B1 before B2), so each pair pairs with both values. That gives 12 combinations.

BEGIN
1 1 0
1 1 1
1 3 0
1 3 1
1 2 0
1 2 1
3 3 0
3 3 1
3 2 0
3 2 1
2 2 0
2 2 1
END