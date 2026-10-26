**Q2 (B2) must be 0.**
- The only writers to x are A3 and B3. B3 writes whatever B2 read.
- Suppose B2 returned a nonzero value v. Then A3 must have taken effect before B2, since A3 is the only other writer of x. B3 then writes v.
- After that, no write of 0 can come before B4, because A3 has already happened. So B4 would return v, which contradicts "returned 0".
- With B2 = 0, B3 writes 0. A3 can take effect between B2 and B3, or after B4 and C4. This keeps B4 = 0 and C4 = 0 consistent with whatever A1 read.

**Q1 (A4) can be 0, 5 or 1.** The writes to z are B1 (5), C2 (5) and C3 (1).
- **A4 = 0:** A1, A2 and A4 all take effect before B1 and C2. A3 then writes 0, which is consistent.
- **A4 = 5:** A4 reads either B1's 5 or C2's 5.
- **A4 = 1:** A4 reads C3's write.

**Q3 (final y) is 3 or 4.** It depends on whether C1 (write 4) or A5 (write 3) takes effect last.
- **A4 = 0:** A4 comes before C2. C1 can still take effect either before or after A5, so y = 3 and y = 4 are both possible.
- **A4 = 5:** If A4 reads B1's 5 while C2 has not yet taken effect, C1 can come after A5, giving y = 4. Otherwise A5 comes last and y = 3.
- **A4 = 1:** The order must be C1 → C2 → C3 → A4 → A5, so A5 is the last write to y and y = 3 only.

BEGIN
0 0 3
0 0 4
5 0 3
5 0 4
1 0 3
END