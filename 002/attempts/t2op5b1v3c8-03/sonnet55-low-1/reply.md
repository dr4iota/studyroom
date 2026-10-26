Each outcome is written as "A5 B3".

**Setup.** Writes to x by A occur in the order 2, 3, 1, 3. Let v2 be the value B2 returns. B4 and B5 both write v2, and both happen after B3. So B3 can only see A's writes (or 0), and it reads at or after B2's time.

**A5 = 3.** No B write lands between A4 and A5. B's writes can come before A4 or after A5. B3 can then be 0, 1, 2 or 3, because it only sees A's writes.

**A5 = 0.** B2 reads 0, so v2 = 0. B4 writes 0 after A4 and before A5. B3 sits between B2 and B4, so it can read 0, 2, 3 or 1, depending on how far A has progressed.

**A5 = 2.** v2 = 2, so B2 reads 2 and B3 comes after it. B3 can be 2, 3 or 1, but not 0.

**A5 = 1.** v2 = 1, so B2 reads 1, which is only possible after A3. B3 can then read 1 (before A4) or 3 (after A4). B4 writes 1 after A4 and before A5.

BEGIN
0 0
0 1
0 2
0 3
1 1
1 3
2 1
2 2
2 3
3 0
3 1
3 2
3 3
END