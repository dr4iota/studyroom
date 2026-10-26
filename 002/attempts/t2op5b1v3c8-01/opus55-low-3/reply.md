The approach is to treat thread A as moving x through a fixed sequence of values, then enumerate by the value B2 reads.

**Setup.** Thread A alone moves x through the states 0 → 1 → 1 → 2 → 3. B1 and B2 both come before any write by B, so each returns one of these states. B2's state is the same as or later than B1's. Let v be the value B2 returns. B3 and B5 both write v.

**B4.** B4 returns either v (from B3) or the value of an A write that took effect between B3 and B4.

**Final value.** If any A write takes effect after B5, then A4 is after B5 and the final value is 3. Otherwise B5 is the last write and the final value is v.

**Linking B4 and the final value.** If B4 returns 3, then A4 came before B4. In that case nothing of A's can follow B5, so the final value is v. Otherwise the final value can be either v or 3.

**Case v = 0.** A has not written anything before B2, so B1 = 0.
- B4 can be 0, 1, 2 or 3.
- The final value is 0 or 3, except that B4 = 3 forces a final value of 0.

**Case v = 1.** B1 is 0 or 1.
- B4 can be 1, 2 or 3.
- The final value is 1 or 3, except that B4 = 3 forces a final value of 1.

**Case v = 2.** B1 is 0, 1 or 2.
- B4 can be 2 or 3.
- B4 = 2 gives a final value of 2 or 3.
- B4 = 3 gives a final value of 2.

**Case v = 3.** B1 can be 0, 1, 2 or 3.
- B4 must be 3.
- The final value must be 3.

BEGIN
0 0 0
0 0 3
0 1 0
0 1 3
0 2 0
0 2 3
0 3 0
0 1 1
0 2 1
0 3 1
1 1 1
1 1 3
1 2 1
1 2 3
1 3 1
0 2 2
0 3 2
1 2 2
1 3 2
2 2 2
2 2 3
2 3 2
0 3 3
1 3 3
2 3 3
3 3 3
END