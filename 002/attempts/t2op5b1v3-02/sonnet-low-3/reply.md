Every interleaving of the two threads is allowed, since there are no sync points. So I track the value of x as a timeline.

**Setup.** Thread B's writes produce the states s0=0, s1=3, s2=2, s3=1, s4=2, in that order. Thread A's reads A1, A2, A3 happen in order, so A2 sees state i and A3 sees state j with i ≤ j. A4 then writes 2 at a point k ≥ j on the timeline. A5 comes after A4, so it either sees A4's 2 (if no B write came in between) or a later B state m > k.

**A5 options by the position k of A4:**
- k=0: A5 can be 1, 2 or 3.
- k=1: A5 can be 1 or 2.
- k=2: A5 can be 1 or 2.
- k=3: A5 can only be 2.
- k=4: A5 can only be 2.

**Combining with (A2, A3).** For A3 at state j, A4 can sit at any k ≥ j, so A5 can take any value allowed for some k ≥ j:
- j=0 gives (0,0), with A5 in {1,2,3}.
- j=1 gives (0,3) and (3,3), with A5 in {1,2}.
- j=2 gives (0,2), (3,2) and (2,2), with A5 in {1,2}.
- j=3 gives (0,1), (3,1), (2,1) and (1,1), with A5 = 2.
- j=4 gives (1,2) with A5 = 2. The other pairs reachable at j=4, namely (0,2), (3,2) and (2,2), are already covered by j=2 and keep A5 in {1,2}.

BEGIN
0 0 1
0 0 2
0 0 3
0 3 1
0 3 2
3 3 1
3 3 2
0 2 1
0 2 2
3 2 1
3 2 2
2 2 1
2 2 2
0 1 2
3 1 2
2 1 2
1 1 2
1 2 2
END