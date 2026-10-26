All writes to x write back a value read from x, so x is always 0: B1 = 0 (and B4 = 0 is automatically satisfied). B2 can be 0 (initial/A5), 2 (C1), or 3 (A4) — never 1, since B5 comes after B2 and C4/C6 could only write 1 after B5. C3 occurs after C1, so it can see 2 (C1), 3 (A4), 0 (A5), or 1 (B5), and each is compatible with A2 reading 2 (e.g. C1, A2, then the relevant writes) and with each B2 value.

BEGIN
0 0 0
0 0 1
0 0 2
0 0 3
0 2 0
0 2 1
0 2 2
0 2 3
0 3 0
0 3 1
0 3 2
0 3 3
END