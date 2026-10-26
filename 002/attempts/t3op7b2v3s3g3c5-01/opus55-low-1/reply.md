Every listed outcome is reachable, and every other combination is ruled out by the steps below.

**1. Time order of the sync points.**
- All of Thread B happens before P.
- A2 ends after P, and A3 and A4 come after A2 and before Q, so P < Q.
- C5 ends after Q, and C6 happens before R, so Q < R.
- A5 and A6 happen after R.

So the order is: all of B, then P, then A3 and A4, then Q, then C6, then R, then A5 and A6.

**2. Final value of y.**
A5 comes after R, which is after every other write to y. So the final y equals a1, the value read by A1.

**3. Possible values of a1.**
A1 happens before P. Before P, the only writes to x are B2 (writes 1) and B4.
- B3 can only see B2's 1, because A3 happens after P. So B3 returns 1 and B4 writes 1.
- Therefore a1 is 0 (if A1 takes effect before B2) or 1 (if after B2).

**4. Possible values of c1, the value read by C1.**
- c1 is 0 if C1 takes effect before B2.
- c1 is 1 if C1 takes effect after B2.
- c1 is also 0 if C1 takes effect after A3 and a1 = 0.

**5. What C7 returning 0 requires.**
The last write to y before C7 must write 0. That write is either C6 (writes c1) or A5 (writes a1). So c1 = 0 or a1 = 0.

**6. A2 returning 3.**
This is always achievable. A2 can see the 3 from B1, C3 or C5, so it adds no restriction.

**7. Values seen by B6 and B7.**
Both reads happen after B5 (writes 2) and before P. The only writes to y they can see are:
- B5, which writes 2;
- C2, which writes c1 and must happen before P;
- C3 or C5, which write 3.

C2, C3 and C5 happen in that order. So once B6 sees a C write, B7 cannot see 2 again. The possible pairs are (2,2), (2,c1), (2,3), (c1,c1), (c1,3) and (3,3).
If B sees C2's value, C1 happened before P. Then c1 is 0 if C1 was before B2, otherwise 1.

**8. Combining the cases.**
- **a1 = 1:** step 5 then needs c1 = 0, so C1 happened before B2. The final y is 1. C7 reads C6's 0 before A5 runs.
- **a1 = 0:** c1 can be 0 or 1. The final y is 0.
  - With c1 = 0, the pairs are the same as in the a1 = 1 case.
  - With c1 = 1, the new pairs are (2,1), (1,1) and (1,3).

BEGIN
2 2 1
2 0 1
2 3 1
0 0 1
0 3 1
3 3 1
2 2 0
2 0 0
2 3 0
0 0 0
0 3 0
3 3 0
2 1 0
1 1 0
1 3 0
END