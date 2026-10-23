All three asked values turn out to be independent of one another:

- **A1** reads y: 0 if it takes effect before B2, 4 if after. (B1 returning 0 is automatic since B2 is the only write to y and follows B1.)
- **B3** reads x: 0 (before A2), 2 (between A2 and A3, or after A5), or 4 (between A3 and A5). B5 comes after B3 so it never affects B3.
- **Final x**: 2 if A5 is the last write, 4 if B5 is. Each B3 placement allows B5 to land either before or after A5 (for B3=2, use the A2–A3 window), so both finals are reachable in every case.

BEGIN
0 0 2
0 0 4
0 2 2
0 2 4
0 4 2
0 4 4
4 0 2
4 0 4
4 2 2
4 2 4
4 4 2
4 4 4
END