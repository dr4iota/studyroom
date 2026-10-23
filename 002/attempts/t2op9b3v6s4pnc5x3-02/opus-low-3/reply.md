The values are A2 ∈ {0, 4}, A3 ∈ {0, 4} (all four pairings) and A7 = 4.

**Ordering from the sync points**
- B1–B6 happen before P, and A4 onward happens after P. So A4–A8 come after B6.
- A1–A3 happen before R, and B7 onward happens after R. So A1–A3 come before B7, B8 and B9. They can interleave freely with B1–B6.
- B8 happens before Q, and A7–A8 happen after Q. So A7 comes after B8.
- B1–B4 happen before S, and A4 onward happens after S. This adds nothing new.

**B5 (read x):** The only write to x that can come before B5 is B3 (4). A4 and A6 come after B6, so they are too late. B5 therefore returns 4.

**Q1, A2 (read z):** The writes to z that can come before A2 are B1 (4) and B6 (B5's value, which is 4). A5 and B9 are too late. So A2 returns 0 or 4.

**Q2, A3 (read x):** The only write to x that can come before A3 is B3 (4). So A3 returns 0 or 4.

**Combining A2 and A3:** All four pairings are possible.
- A2 = 4 with A3 = 0 works with the order B1 < A2 < A3 < B3.
- A2 = 0 with A3 = 4 works with the order A2 < B1 … B3 < A3.
- The other two pairings are equally easy to arrange.

**Q3, A7 (read y):** B2 (2) and B8 (4) both come before A7. B8 comes after B2, so it is the last write before A7. A8 comes after A7. So A7 always returns 4.

BEGIN
0 0 4
0 4 4
4 0 4
4 4 4
END