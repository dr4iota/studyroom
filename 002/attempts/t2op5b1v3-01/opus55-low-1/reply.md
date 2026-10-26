**Approach.** Each read returns the value of the most recent write that took effect before it. A1 can only see B1 or B4, since A3 and A4 come after it. B3 can see B1, A3 or A4. B5 can see B4, A3 or A4.

**Q1 (A1).**
- If A1 takes effect before B1, it returns 0.
- Otherwise it returns 1, because both B1 and B4 write 1.
- A1's timing only limits it to coming before A3. Placing A1 either just before or just after B1 leaves every arrangement of the other operations open. So both A1 values combine with every (B3, B5) pair below.

**Q2 and Q3 (B3, B5).**
- **B3 = 1:** A3 and A4 both take effect before B1 or after B3.
  - B5 = 1: A3 and A4 both take effect before B4 or after B5.
  - B5 = 2: A3 takes effect between B4 and B5, and A4 after B5.
  - B5 = 3: A4 takes effect between B4 and B5.
  - So B5 can be 1, 2 or 3.
- **B3 = 2:** A3 takes effect before B3, and A4 after B3.
  - B5 = 3: A4 takes effect between B4 and B5.
  - B5 = 1: A4 takes effect before B4 or after B5.
  - B5 = 2 is impossible, because A3 cannot come after B4 here.
  - So B5 can be 1 or 3.
- **B3 = 3:** A4 takes effect before B3, so both A writes come before B4. B5 can only be 1.

This gives six (B3, B5) pairs: (1,1), (1,2), (1,3), (2,1), (2,3), (3,1). Each combines with A1 = 0 or A1 = 1, for 12 outcomes.

BEGIN
0 1 1
0 1 2
0 1 3
0 2 1
0 2 3
0 3 1
1 1 1
1 1 2
1 1 3
1 2 1
1 2 3
1 3 1
END