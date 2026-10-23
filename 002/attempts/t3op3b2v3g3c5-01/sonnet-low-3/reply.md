Write order on x: C1 < C2 < C3. Since C3 returns 2, A2 (the only write of 2) must take effect after C2 and before C3. So B3 cannot fall between A2 and C3, because it would then be the last write and C3 would return 3.

**B3 before A2 (final x = 2):**
- B1 happens before B3, so B1 sees only 0, 1 or 3. It cannot see 2.
- A1 happens before A2, so it sees 0, 1 or 3.
- A1 and B1 can be placed independently, so all 9 pairs are possible.

**B3 after C3 (final x = 3):**
- A1 sees 0, 1 or 3.
- B1 can also fall after A2, so it sees 0, 1, 2 or 3.
- All 12 pairs are possible.

BEGIN
0 0 2
0 1 2
0 3 2
1 0 2
1 1 2
1 3 2
3 0 2
3 1 2
3 3 2
0 0 3
0 1 3
0 2 3
0 3 3
1 0 3
1 1 3
1 2 3
1 3 3
3 0 3
3 1 3
3 2 3
3 3 3
END