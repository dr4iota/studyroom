Reasoning: thread A's writes to y happen in the order 2, 1, 1, then x=3, then y=1. Let r1 be what B1 reads, r3 what B3 reads, and r5 what B5 reads.

- B1 can read 0, 2 or 1.
- After B2, x holds r1 until A4 writes 3. So B3 returns r1 or 3, and B5 returns r1 or 3. If B3 returned 3, B5 also returns 3.
- The final y is either 1, when A5 is last, or r3, when B4 is last. B4 can be last only if A5 comes before it, which forces A4 to come before B4.

Cases by r1:
- **r1=0:**
  - B3=0 and B5=0 forces A4 after B5, so A5 is last and y=1. This gives (0,0,1).
  - B3=0 and B5=3 gives y=1, or y=0 if B4 runs after A5. This gives (0,3,1) and (0,3,0).
  - B3=3 gives B5=3 and y=1 or 3. This gives (3,3,1) and (3,3,3).
- **r1=2:**
  - B3=2 and B5=2 gives y=1, so (2,2,1).
  - B3=2 and B5=3 gives y=1 or 2, so (2,3,1) and (2,3,2).
  - B3=3 gives (3,3,1) and (3,3,3), already listed.
- **r1=1:**
  - B3=1 and B5=1 gives y=1, so (1,1,1).
  - B3=1 and B5=3 gives y=1, so (1,3,1).
  - B3=3 gives (3,3,1) and (3,3,1), already listed (here B4 writes 3 and A5 then writes 1, or A5 comes first and B4 writes 3, which would give y=3, already listed).

BEGIN
0 0 1
0 3 0
0 3 1
3 3 1
3 3 3
2 2 1
2 3 1
2 3 2
1 1 1
1 3 1
END