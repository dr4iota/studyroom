Every listed combination is possible, and no others are.

**Constraints**
- A1 and B1 always return 0, because no thread ever writes y and B1 can take effect before any write to x.
- B2's start and end are before P.
- A2's end is after P.
- A2's start can be before P. So A2 can take effect at any instant after A1, including before B2.
- The writes to x come in a fixed order within thread B: B2 writes 3, then B3 writes 2, then B4 writes 1. A4 writes whatever A3 read, and it can take effect anywhere after A3.

**What each read can return**
- A2 sees the latest B write that took effect before it. That can be none (0), B2 (3), B3 (2) or B4 (1).
- A3 takes effect after A2, so it returns the value A2 saw or a later one in the sequence 0 → 3 → 2 → 1.

**Final value of x**
- If A4 takes effect after B4, the final value is the value A3 read.
- If A4 takes effect before B4, B4 overwrites it and the final value is 1.
- When A3 returned 1, both cases give a final value of 1.

**Combinations by A2's result**
- **A2 = 0:** A3 can return 0, 3, 2 or 1. This gives (0,0,0), (0,0,1), (0,3,3), (0,3,1), (0,2,2), (0,2,1) and (0,1,1).
- **A2 = 3:** A3 can return 3, 2 or 1. This gives (3,3,3), (3,3,1), (3,2,2), (3,2,1) and (3,1,1).
- **A2 = 2:** A3 can return 2 or 1. This gives (2,2,2), (2,2,1) and (2,1,1).
- **A2 = 1:** A3 must return 1. This gives (1,1,1).

BEGIN
0 0 0
0 0 1
0 3 3
0 3 1
0 2 2
0 2 1
0 1 1
3 3 3
3 3 1
3 2 2
3 2 1
3 1 1
2 2 2
2 2 1
2 1 1
1 1 1
END