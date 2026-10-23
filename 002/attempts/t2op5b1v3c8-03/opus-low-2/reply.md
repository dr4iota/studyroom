Every execution behaves as if the operations of both threads happen one at a time in some interleaving that keeps each thread's order. Below I write "earlier" and "later" for the order in which operations take effect.

**The values A's writes leave in x.** Thread B does not write until B4. So while B1–B3 run, x moves through the states 0 → 2 (after A1) → 3 (after A2) → 1 (after A3) → 3 (after A4). Call these states s0 to s4.

**B2 and B3.** B2 reads some state si. B3 reads a state sj with j ≥ i, because B3 takes effect later than B2. Let v = si be the value B2 read. B4 and B5 both write v.

**A5.** A5 reads either the 3 written by A4 or the v written by B4 or B5:
- A5 returns 3 if no B write takes effect between A4 and A5. For example, B4 and B5 are both later than A5. Any value of B3 is still possible here.
- A5 returns v if B4 or B5 takes effect after A4 and before A5. Nothing stops B1–B3 from all taking effect before A4 as well, so any i ≤ j works.

**Combinations, listed as (A5, B3):**
- **A5 = 3:** B3 can be 0, 2, 3 or 1.
- **i = 0 (v = 0):** B3 can be any state, giving (0,0), (0,2), (0,3), (0,1).
- **i = 1 (v = 2):** B3 is s1 to s4, giving (2,2), (2,3), (2,1).
- **i = 2 (v = 3):** B3 is s2 to s4, giving (3,3) and (3,1). Both already appear above.
- **i = 3 (v = 1):** B3 is s3 or s4, giving (1,1) and (1,3).
- **i = 4 (v = 3):** B3 is 3, giving (3,3), already listed.

BEGIN
3 0
3 2
3 3
3 1
0 0
0 2
0 3
0 1
2 2
2 3
2 1
1 1
1 3
END