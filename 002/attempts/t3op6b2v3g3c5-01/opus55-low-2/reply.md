The operations have no sync points, so any interleaving that keeps each thread's program order works. The answer comes from listing which value each asked read can see, then checking that each combination has a valid ordering.

**Q1 (A1).** The writes to x are C1=2, B2=2, B3=3, B4=2, and A5. A5 comes after A1 in thread A, so A1 can only see the initial 0 or a 2 or 3 from B or C.
- A1 = 0: A1 happens before every write to x. A3 later sees 2 from C1, B2 or B4.
- A1 = 2: A1 happens after a 2-write such as C1.
- A1 = 3: A1 happens after B3. A3 then sees the 2 from B4.

**Q2 (C2).** C2 comes after C1, so x is no longer 0 from the initial state. C2 can see 2 (from C1, B2 or B4) or 3 (from B3). It can also see what A5 wrote, which is A1's value.
- When A1 = 0, A5 writes 0. If A5 happens after A3 has read 2 and before C2, then C2 returns 0.
- When A1 = 2 or 3, A5 only rewrites a 2 or 3, so C2 cannot be 0.

**Q3 (C4).** The writes to y are B5=2 and C5=1. C5 comes after C4 in thread C, so C4 sees either 0 or B5's 2.
- B1 reading 0 only requires B1 to come before B5 and C5, which program order and the schedules below allow.
- C4 = 2: B5 happens before C4.
- C4 = 0: C4 happens before B5.

**Witness schedules** for the less obvious cases:
- **A1=0, C2=0, C4=2:** A1, B1, B2, B3, B4, B5, C1, A2, A3 (reads 2), A4, A5 (writes 0), C2 (reads 0), C3, C4 (reads 2), C5.
- **A1=0, C2=0, C4=0:** A1, C1, B1, B2, B3, B4, A2, A3 (reads 2), A4, A5 (writes 0), C2 (reads 0), C3, C4 (reads 0), B5, C5.
- **C2=3:** C2 is placed between B3 and B4. B5 then goes either before or after C4. This works for each value of A1, and A3 still reads 2.

Every other pairing can be scheduled the same way, giving 14 combinations. For A1 = 0 there are three C2 values times two C4 values. For A1 = 2 and A1 = 3 there are two C2 values times two C4 values each.

BEGIN
0 0 0
0 0 2
0 2 0
0 2 2
0 3 0
0 3 2
2 2 0
2 2 2
2 3 0
2 3 2
3 2 0
3 2 2
3 3 0
3 3 2
END