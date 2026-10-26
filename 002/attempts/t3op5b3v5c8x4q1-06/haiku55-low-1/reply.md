**Key constraints**

- **Final y = 0:** The only writes to y are A1 (3), C1 (3), and B2 (the value B1 read). Since no write can produce 0 except B2 with B1 = 0, B2 must be the last write to y, and B1 must have read 0. So B1 takes effect before A1 and C1.
- **Final x = 3:** The only writes to x are C2 (5) and C5 (the value C3 read). Final x = 3 requires C5 to be the last x-write and C3 to have read 3.
- **C3 reads 3:** The last write to y before C3 must be 3 (from C1 or A1). Since B2 is the last y-write, C3 must take effect before B2.
- **B4's possible values:** Thread order gives C2 < C3 < B2 < B4, so C2 always takes effect before B4, ruling out 0. The last x-write before B4 is then either C2 (value 5, if C5 comes after B4) or C5 (value 3, if C5 comes before B4).

**Both outcomes are feasible.** For example, the order B1, C1, C2, C3, A1, B2, B3, B4, C4, C5 gives B4 = 5. Moving C4 and C5 before B4 gives B4 = 3. In both, the final values are x = 3 and y = 0.

So B4 can return 3 or 5.

BEGIN
3
5
END