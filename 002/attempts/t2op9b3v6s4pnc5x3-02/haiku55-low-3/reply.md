The possible outcomes are below. Q3 is always 4, and Q1 and Q2 each take both values 0 and 4, independently of each other.

**Q3 (A7) is always 4.** Program order and the sync lines force B8 < Q < A7. B8 writes 4 to y, and the only other write to y before A7 is B2 (2), which precedes B8. A8 writes to y only after A7.

**Q2 (A3) is 0 or 4.** The only write to x that can precede A3 is B3 (writing 4). A4 and A6 are after P, which is after B5, and B5 is after B3. Each value is feasible. For 0, A3 runs before B3. For 4, B3 runs before A3.

**Q1 (A2) is 0 or 4.** The only writes to z that can precede A2 are B1 and B6, both writing 4. A5 and B9 are ordered after A2 (B9 is after R, which is after A2). Each value is feasible. For 0, A2 runs before B1. For 4, B1 runs before A2.

Each of the four combinations has an explicit schedule, for example:
- (0,0): A1 A2 B1 A3 R B2 B3 B4 S … with A3 before B3.
- (4,0): B1 is before A2, and A3 is before B3.
- (0,4): A2 is before B1, and B3 is before A3.
- (4,4): B1 is before A2, and B3 is before A3.

BEGIN
0 0 4
0 4 4
4 0 4
4 4 4
END