Only two combinations are possible: y can end as 0 or 4, and z always ends as 3.

**Thread A's read of x.** A3 returns 0, and A2 wrote the value read by A1 to z just before it. Every other write to z (2, 4, 5, 3) is nonzero. So A1 must have read 0, and A2 wrote 0. It follows that A4, A5 and A7 all write 0.

**Writes to y.** The writes to y are A5 (0), A7 (0) and B4 (4). C5 returns 4, so B4 precedes C5, and no write of 0 from A may fall between B4 and C5.

**Writes of 4 to x.** C7 writes 4 to x, since C5 returned 4. It is the only write of 4 to x. B7 and A8 both read 4, so both come after C7. A8 reading 4 also means C7 comes after A4, which wrote 0 to x.

**Final z.**
- B8 reads z after C7, which comes after A4 and therefore after A2.
- B8 returns 3, so a write of 3 (B5 or C3) must come after A2.
- That makes A2's 0 not the last write to z.
- B1's 2 comes before B5's 3, so 2 cannot be last either.
- Writes 4 and 5 (C1, C2) come before C3's 3, so they cannot be last.
- Hence z ends as 3.

**Final y.** Both values can be realised:
- **y = 4:** the order is A1 to A7, then B4, then C5, then C7, then A8. This puts B4 after A7 and keeps every other constraint satisfied.
- **y = 0:** B4 and C5 happen before A5, and A7 is the last write to y. The 0 from A7 ends up as the final value.

BEGIN
0 3
4 3
END