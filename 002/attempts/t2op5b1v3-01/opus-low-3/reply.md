Under these rules each operation takes effect at a single instant. So every execution is an interleaving of A1–A4 with B1–B5, with each thread keeping its own order. There are no sync points, so any such interleaving is allowed.

**Q1 (A1):** A1 takes effect before A's own writes A3 and A4. So it can only see the initial 0 or a 1 written by B.
- A1 = 0 if A1 takes effect before B1.
- A1 = 1 if A1 takes effect after B1.

B4 cannot be the source, because B4 comes after B3 and the cases below never need it before A1. So A1 ∈ {0, 1}.

**Q2 (B3):** B3 returns the last write before it, which is one of B1 (1), A3 (2) or A4 (3).
- **B3 = 1:** A3 and A4 both take effect after B3 (or A3 also lands before B1 when A1 = 0).
  - B5 = 1 if both A writes come after B5, or both come before B4.
  - B5 = 2 if A3 is between B4 and B5, and A4 is after B5.
  - B5 = 3 if A4 is between B4 and B5.
- **B3 = 2:** A3 takes effect before B3 and A4 after B3.
  - B5 = 1 if A4 is before B4 or after B5.
  - B5 = 3 if A4 is between B4 and B5.
  - B5 = 2 is impossible, because A3 already happened before B4.
- **B3 = 3:** A4 takes effect before B3, so there are no A writes left after B4. B5 = 1.

**Combining with Q1:** A1 only constrains where A1 sits relative to B1. A1 can always be placed early enough (before or after B1) without restricting where A3 and A4 go. So both values of A1 work with all six (B3, B5) pairs.

BEGIN
0 1 1
0 1 2
0 1 3
0 2 1
0 2 3
0 3 1
1 1 1
1 1 2
1 1 3
1 2 1
1 2 3
1 3 1
END