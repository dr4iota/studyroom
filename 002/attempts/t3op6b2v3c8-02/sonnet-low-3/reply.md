Outcomes are written as (A4, C2, C4).

**Which values each read can return**

- C2 reads y after C1 has written 1. It can return 1 (C1's own write) or 2 (B1's write). It can also return 0. For that, A1 reads 0 before C1 and B1 act, and A3 then writes that 0 to y after C1 and before C2.
- C4 reads x after C3 has written C2's value to x. The only other writer of x that can land before C4 is B2, which writes 1. C6 comes after C4 in thread C. So C4 returns either C2's value or 1.
- A4 reads x and can see 0 (before any write to x), 1 (after B2), or 2 (after C6, or after C3 when C2 returned 2).

**Case C2 = 0**

C3 writes 0 to x, and B2 runs only after C2 because B1 is after A1's read of 0. C4 can be 0 or 1.

- C4 = 0 is reached when C4 runs before B2, or when B2 runs and then C3 overwrites it with 0.
- C4 = 1 is reached when B2 lands between C3 and C4.

Every A4 value works with each C4 value:

- A4 = 0 comes from reading before B2.
- A4 = 1 comes from reading after B2. With C4 = 0 this needs the order C2, B2, A4, C3, C4.
- A4 = 2 comes from reading after C6.

This gives 6 combinations.

**Case C2 = 1**

C3 writes 1 and B2 also writes 1, so C4 must be 1. A4 can be 0, 1 or 2, giving 3 combinations.

**Case C2 = 2**

C4 = 2 when no B2 write lands between C3 and C4. C4 = 1 when B2 does land between them. A4 can be 0, 1 or 2 in both sub-cases. For A4 = 1 with C4 = 2, the order is B2, A4, C3, C4. This gives 6 combinations.

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