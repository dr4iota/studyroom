The possible outcomes are the nine combinations below. Each thread's operations take effect in program order, so every execution is an interleaving of the three sequences.

- **Q2 (C2):** Thread C writes y=1 at C1 before C2, so C2 can never read 0. The reads 1 and 2 are both achievable (C1 then C2 with no y-write between them; or C1, B1, C2).
- **Q3 (C4):** C4 sees the last x-write before it. C6 comes after C4, so only B2 (value 1) and C3 (value c2) matter. So Q3 is c2, or 1 if B2 falls between C3 and C4.
- **Q1 (A4):** A4 sees the last x-write before it, which is 0 (none yet), 1 (B2), c2 (C3), or 2 (C6).

Checking each candidate against an explicit interleaving:

- c2=1, c4=1: A4 reads 0, 1, or 2 (e.g. A1–A4 first; B1, B2 then A1–A4; C1–C6 then A1–A4).
- c2=2, c4=2: A4 reads 0, 1, or 2 (e.g. C1, B1, C2, C3, C4, then A1–A4 with B2 later for 0 or 1).
- c2=2, c4=1: A4 reads 0, 1, or 2 (e.g. C1, B1, C2, C3, B2, C4 with A4 placed before or after as needed).

BEGIN
0 1 1
0 2 1
0 2 2
1 1 1
1 2 1
1 2 2
2 1 1
2 2 1
2 2 2
END