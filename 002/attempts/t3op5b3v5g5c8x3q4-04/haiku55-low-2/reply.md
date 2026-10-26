The possible outcomes are the five combinations below. Q2 is always 0, because B2 can only see A3's write if it happens before B3 overwrites x, and then B4 would read a nonzero value. Q1 can be 0, 1, or 5. Final y is 4 only when A5 comes before C1, which requires A4 to come before C1, so Q1 = 1 forces final y = 3.

Example schedules (instant order):
- **0 0 3:** C1, A1, A2, A3, A4, A5, C2, C3, C4, B1, B2, B3, B4
- **0 0 4:** A1, A2, A3, A4, A5, C1, C2, C3, C4, B1, B2, B3, B4
- **1 0 3:** B1, B2, A1, C1, C2, C3, A2, A3, A4, B3, B4, C4, A5
- **5 0 3:** B1, B2, A1, A2, A3, B3, B4, A4, C1, C2, C3, C4, A5
- **5 0 4:** B1, B2, A1, A2, A3, B3, B4, A4, A5, C1, C2, C3, C4

BEGIN
0 0 3
0 0 4
1 0 3
5 0 3
5 0 4
END