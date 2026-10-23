I checked this by reasoning about the possible orderings of the operations, not by running code. Every value that appears is 0, 2, or 3. Value 2 can only enter the x-block through B4 when B2 reads 2 from A1, so the outcomes split into two families. One family uses only 0 and 3. The other has B4 writing 2, which produces the combinations containing 2. The 16 outcomes below each have an explicit ordering that realizes them.

Values are listed in the order asked: Q1 = A2, Q2 = B1, Q3 = C4.

BEGIN
0 0 0
0 0 2
0 0 3
0 3 0
0 3 2
0 3 3
2 0 2
2 0 3
2 3 2
2 3 3
3 0 0
3 0 2
3 0 3
3 3 0
3 3 2
3 3 3
END