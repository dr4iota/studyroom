Five outcomes are possible for (Q1, Q2, Q3, Q4), where Q4 always equals Q2.

**Key facts**
- A2 always reads 0 from z, since every write to z by B occurs after A2, and A6 comes after A2.
- B5 writes Q2 to y, and it always takes effect after A5. So B9 always reads Q2 from y, giving Q4 = Q2.
- A8 always follows A7, so A8 reads either A7's 0 or B1's 5. It cannot read 3.
- B8 always follows A3, so it reads 0 or 5. It cannot read 3.
- Q2 can be 0, 3, or 5, depending on where B1 falls in the x-write order (A1=3, A3=0, A7=0, B1=5).

**Case analysis on where B1 falls among the A-writes to x**
- B1 before A1: Q1=0, Q3=0, and Q2 is 3 or 0. This gives (0,3,0) and (0,0,0).
- B1 between A1 and A3: Q1=0, Q3=0, and Q2 is 5 or 0. This gives (0,5,0) and (0,0,0).
- B1 between A3 and A7: Q1=0, and (Q2, Q3) is (5,5), (5,0), or (0,0). This gives (0,5,5), (0,5,0), and (0,0,0).
- B1 after A7: Q2=5 and Q3=5 are forced, and Q1 is 5 or 0. This gives (5,5,5) and (0,5,5).

I checked a concrete schedule for each of the five outcomes against all the sync constraints.

BEGIN
0 0 0 0
0 3 0 3
0 5 0 5
0 5 5 5
5 5 5 5
END