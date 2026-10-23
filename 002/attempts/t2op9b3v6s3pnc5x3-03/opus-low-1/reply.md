**Ordering constraints from the sync points**
- A1–A5 happen before R, and B5 happens after R.
- A6–A7 happen before P, and B8–B9 happen after P.
- A8–A9 happen before Q, and B6–B9 happen after Q.
- So B6–B9 all come after every operation of thread A.

**Final value of z (Q3)**
- B9 is the last write to z, so the final z equals the value read by B2.
- B2 comes before B3, so B2 cannot see 3 from B3.
- B2 also cannot see 3 written by A9. A9 writes 3 only if A6 read 3. That needs B3 before A6, which puts B2 before A9.
- So B2 reads 0 (before A3) or 5 (from A3, or from A9 when A6 read 5).
- **Final z is 0 or 5.**

**Value returned by A1 (Q1)**
- A1 can only see a write by B3, since thread A writes z only at A3 and A9, which come later.
- So A1 returns 0, or 3 if B3 happened before A1.

**Value returned by A5 (Q2)**
- A4 writes A2's value to x. B1 can write 5 to x between A4 and A5. B7 comes after all of thread A.
- So A5 returns either A2's value or 5.
- A2 returns 3 if B3 came before it, otherwise 0.

**Combining the cases**

If A1 = 3:
- Then B2 < B3 < A1 < A3, so B2 reads 0 and the final z is 0.
- A2 reads 3, so A5 is 3 or 5.
- Outcomes: (3, 3, 0) and (3, 5, 0).

If A1 = 0 and the final z is 0:
- B2 happens before A3, and B3 can fall anywhere after B2.
- So A2 can be 0 or 3, and A5 can be 0, 3 or 5.
- Outcomes: (0, 0, 0), (0, 3, 0) and (0, 5, 0).

If A1 = 0 and the final z is 5:
- B2 happens after A3, so B3 also comes after A3, and therefore after A2.
- So A2 reads 0, and A5 is 0 or 5.
- Outcomes: (0, 0, 5) and (0, 5, 5).

BEGIN
0 0 0
0 3 0
0 5 0
0 0 5
0 5 5
3 3 0
3 5 0
END