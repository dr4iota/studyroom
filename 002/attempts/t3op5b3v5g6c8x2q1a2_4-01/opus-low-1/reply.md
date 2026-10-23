The possible final values of z are **2** and **4**.

1. **y stays 0, so B2 writes 0 to z.** The only write to y is B3, which comes after B1 in thread B. So B1 reads y = 0. That means B2 writes 0 to z and B3 writes 0 to y.

2. **The writes to z are:** A1 writes 2, B2 writes 0, C1 writes 1 and C2 writes 4.

3. **B4 reading 4 means C2 is the last write to z before B4.** So B2 must take effect before C2, since B2 also comes before B4 in thread B. C1 is always before C2 in thread C. A1 must take effect either before C2 or after B4.

4. **Possible last writes to z:**
   - **C2 (value 4):** Put A1, B2 and C1 all before C2. Then x and the other reads are unaffected, so A3 and A4 can still read x = 1.
   - **A1 (value 2):** Let A1 take effect after B4. A1 is thread A's first operation, so all of thread A then runs after B4. A2, A3 and A4 then run in order with no other writes to x, so they read 1 as required.
   - **B2 or C1:** Neither can be last, because both always take effect before C2.

BEGIN
2
4
END