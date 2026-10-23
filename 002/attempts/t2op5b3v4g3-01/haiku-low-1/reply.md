The possible outcomes are the 12 combinations below. Y is written only by B1, so "A3 returns 4" forces B1 to take effect before A3. The only writes to z that can precede B2 or B3 are A2 (writes 3) and A4 (writes 4), since B5 comes after B3. A1 returns 0 if it takes effect before B1 and 4 otherwise. Every combination of (A1, B2, B3) in the list is realized by some interleaving that satisfies the ordering rules.

BEGIN
0 4 4
0 3 4
0 3 3
0 0 4
0 0 3
0 0 0
4 4 4
4 3 4
4 3 3
4 0 4
4 0 3
4 0 0
END