Values below are listed as (A3 result, final x, final y).

**Step 1: what B2 reads (call it b).** B2 runs after B1, so it sees either B1's 2 or C4's 1. It sees 1 only if C4 takes effect between B1 and B2. So b is 1 or 2, and B3, B4 and B5 all write b.

**Step 2: final y.** The last write to y is either B3 (writes b) or C4 (writes 1). If b = 1, then C4 came before B2, so B3 is later and y = 1. Final y = 2 is possible only when b = 2 and B3 takes effect after C4.

**Step 3: final x.** The last write to x is one of these:
- A5 makes x = 3.
- B5 makes x = b.
- C2 makes x equal whatever C1 read. That can be 0, 1, 3, A3's value, or b.

If C2 is last, then C4 (after C2) is after B5, which is after B3. So y = 1 whenever C2 is the last write to x.

**Step 4: A3's value.**

*A3 reads 0* (A3 takes effect before B1 and before C4).
- x = 3 or x = 2 can occur with y = 1 or y = 2.
- x = 1 occurs through B5 with b = 1, or through C2 copying A1's 1. Either way y = 1.
- x = 0 occurs when C1 reads before A1 and C2 is last, so y = 1.
- Results: (0,3,1), (0,3,2), (0,2,1), (0,2,2), (0,1,1), (0,0,1).

*A3 reads 2* (A3 takes effect after B1, before any write of 1 to y).
- b can still be 1, because C4 can land after A3 but before B2.
- The cases match the A3 = 0 case.
- Results: (2,3,1), (2,3,2), (2,2,1), (2,2,2), (2,1,1), (2,0,1).

*A3 reads 1* (C4 takes effect before A3, directly or through B3 when b = 1).
- x = 0 is impossible. It would need C2 last after A5, which puts C4 after A3. But C4 must come before A3, which is a contradiction.
- x = 3 and x = 2 work with y = 1 or y = 2.
- x = 1 works with y = 1.
- Results: (1,3,1), (1,3,2), (1,2,1), (1,2,2), (1,1,1).

BEGIN
0 3 1
0 3 2
0 2 1
0 2 2
0 1 1
0 0 1
2 3 1
2 3 2
2 2 1
2 2 2
2 1 1
2 0 1
1 3 1
1 3 2
1 2 1
1 2 2
1 1 1
END