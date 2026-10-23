The possible outcomes are (Q1, Q2, Q3) = (0,0,0), (0,0,5), (0,3,0), (0,5,0), (0,5,5), (3,3,0), and (3,5,0).

**Constraints from the sync points.** A1–A5 are before R, A1–A7 before P, and A1–A9 before Q. B5–B9 are after R, B6–B9 after Q, and B8–B9 after P. So the only ordering requirements are A5 < B5, A7 < B8, and A9 < B6. In particular, B6–B9 all come after A9, and B1–B4 are otherwise free.

**Key facts.**
- Q1 (A1 reads z): the only z-write that can precede A1 is B3, so Q1 ∈ {0, 3}, with Q1 = 3 exactly when B3 precedes A1.
- A2 reads z the same way, so A2 ∈ {0, 3}, with A2 = 3 exactly when B3 precedes A2. Q1 = 3 forces A2 = 3.
- Q2 (A5 reads x): the x-writes before A5 are B1 (value 5) and A4 (which writes A2's value). B7 comes after A9, so it is too late. So Q2 = 5 if A4 < B1 < A5, and otherwise Q2 = A2's value.
- Final z: B3 precedes B9 and A3, A9 precede B9, so the last z-write is B9, which writes B2's value. Hence Q3 = value of B2. B2 precedes B3, and A3 always precedes A6, which sees 5 or 3. If B2 is after A9, then B3 is after A6 too, so A6 = 5. So Q3 ∈ {0, 5}, with Q3 = 5 exactly when B2 is after A3.

**Checking the 9 combinations of (Q1, Q2) against Q3.** Since B2 < B3 always:
- Q1 = 3 forces B2 < B3 < A1 < A3, so Q3 = 0. That leaves (3,3,0) and (3,5,0), and (3,·,5) is impossible.
- Q1 = 0, Q2 = 3 forces B2 < B3 < A2 < A3, so Q3 = 0. That leaves (0,3,0), and (0,3,5) is impossible.
- The remaining cases (Q1 = 0 with Q2 = 0 or 5) allow either Q3 value. Each is realised by an explicit ordering, for example:
  - (0,0,5): A1, A2, A3, B2, A4…A9, then B3 and the rest.
  - (0,5,5): A1, A2, A3, A4, B1, A5, B2, B3, then the rest.

Every combination listed above has a valid ordering. I found no others.

BEGIN
0 0 0
0 0 5
0 3 0
0 5 0
0 5 5
3 3 0
3 5 0
END