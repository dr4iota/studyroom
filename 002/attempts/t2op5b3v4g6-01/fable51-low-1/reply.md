The only contended block is y (B2 always sees x=0, so it imposes no constraint). A's writes to y are A1=3, A3=4, A4=3; B's are B4=1, B5=2.

- Q1 (A2): reads after A1, so 3 unless B4 (→1) or B5 (→2) lands between A1 and A2.
- Q2 (B3): 0 if before A1, 3 after A1/A4, 4 between A3 and A4.
- Q3: last of A4 (3) or B5 (2).

Constraints: if Q1=2, B5 precedes A2 and hence A4, so final is 3. If Q1∈{1,2}, B3 precedes B4 which precedes A3, so Q2 can't be 4. Everything else is free.

BEGIN
3 0 3
3 0 2
3 3 3
3 3 2
3 4 3
3 4 2
1 0 3
1 0 2
1 3 3
1 3 2
2 0 3
2 3 3
END