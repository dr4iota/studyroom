**Analysis**

- Final z = 1 means B1 (write 1 to z) is the last z-write, so all of A and C (A5, A7, C2, C8) finish before B1. Hence all of thread B runs after A and C complete; B's constraints (B2=B7=4, B6: x=4) just require y=4 and x=4 at that time, which hold below.
- C3 reads 5 and C4 reads 4 force the y-write order C1 < C3 < A4 < C4, with A1 not between C1 and C3.
- A3 (read y) lies between A1 and A4: if A1 < C1 it can read 1 (before C1) or 5 (after C1); if A1 is after C3 it reads 1. So A3 ∈ {1, 5}.
- C6 occurs after C4 > A4, and A4 is the last write to y among A and C, so C6 = 4 always (which also makes x final = 4, satisfying B6).

BEGIN
1 4
5 4
END