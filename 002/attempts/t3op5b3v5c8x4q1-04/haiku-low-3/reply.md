Final z can be **4** or **5**. Enumerating the executions consistent with the known result (A4 reads 5):

- A4 must see 5, and the only 5-writes are A1 and C5 (B2 can't be 5, since B1 would need x=5, which requires A5, which comes after A4). So C4 must read 5 from A1, and C5 must write that 5 after A2 and before A4.
- This forces the z-timeline C2 < A1 < C4 < A2 < C5 < A4, with B2 and B3 kept out of the windows (A1, C4) and (C5, A4).
- B3 is never overwritten by B2, so B2 can never be the last z-write. The last z-write is either C5 (value 5) or B3 (value 4). Final values 3 are impossible because C5 always follows A2 and C2.

Both outcomes are feasible:
- **5:** B1, B2, B3 all run before C2, so C5 is last.
- **4:** B1 and B2 run first, and B3 runs after A4.

BEGIN
4
5
END