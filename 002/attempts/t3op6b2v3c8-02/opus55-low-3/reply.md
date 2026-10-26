Every combination with C2 ∈ {0, 1, 2}, C4 ∈ {C2, 1} and A4 ∈ {0, 1, 2} is possible, giving 15 combinations. There are no sync points here, so every interleaving that respects each thread's order is allowed.

**Q2: the value returned by C2.** C2 reads y after C1.
- **1:** C1 is the last write to y before C2.
- **2:** B1 takes effect after C1 and before C2.
- **0:** A1 reads y before both B1 and C1, so it returns 0. A3 then writes that 0 to y after C1 and just before C2.

So C2 can return 0, 1 or 2. Call this value c.

**Q3: the value returned by C4.** C4 reads x after C3 (which writes c to x) and before C6.
- **c:** B2 takes effect before C3, or after C4.
- **1:** B2 (write 1 to x) takes effect between C3 and C4.

**Q1: the value returned by A4.** The possible values are 0 and every value ever written to x: 1 from B2, c from C3, and 2 from C6. Since c is itself 0, 1 or 2, A4 ∈ {0, 1, 2}. Each choice fits with every choice of C2 and C4:
- **A4 = 0:** A4 takes effect before both B2 and C3. For c = 0, the order A1, C1, A2, A3, C2, A4 then lets the rest proceed freely.
- **A4 = 1:** B2 is the last write to x before A4. This works whether B2 falls before C3 or between C3 and C4.
- **A4 = 2:** C6 takes effect before A4. This works for every c and both C4 outcomes.

**Count.**
- c = 0: A4 ∈ {0, 1, 2} and C4 ∈ {0, 1}, giving 6 combinations.
- c = 1: A4 ∈ {0, 1, 2} and C4 = 1, giving 3 combinations.
- c = 2: A4 ∈ {0, 1, 2} and C4 ∈ {1, 2}, giving 6 combinations.

BEGIN
0 0 0
0 0 1
1 0 0
1 0 1
2 0 0
2 0 1
0 1 1
1 1 1
2 1 1
0 2 1
0 2 2
1 2 1
1 2 2
2 2 1
2 2 2
END