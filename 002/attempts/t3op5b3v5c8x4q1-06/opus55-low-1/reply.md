**Q1 (the value returned by B4) can be 3 or 5.**

1. **Why B1 must return 0.** The writes to y are A1 (3), C1 (3) and B2 (the value read by B1). For y to end at 0, the last write must be B2, and B1 must have returned 0. So B1 takes effect before both A1 and C1, and B2 takes effect after both.

2. **Why C3 must return 3.** The writes to x are C2 (5) and C5 (the value read by C3). For x to end at 3, C5 must be the last write and C3 must have returned 3. C3 follows C1 in its own thread, so C3 must also take effect before B2. Otherwise it would read B2's 0.

3. **What B4 can see.** B4 follows B2 in thread B. From step 2, B2 follows C3, which follows C2. So C2's 5 is already in x when B4 runs. Whether B4 also sees C5's 3 depends on the order of B4 and C5:
   - **B4 returns 5:** C3 → B2 → B3 → B4, and then C4 → C5 last.
   - **B4 returns 3:** C3 → C4 → C5 → B2 → B3 → B4.

   Both orders keep the final values x = 3 and y = 0.

BEGIN
3
5
END