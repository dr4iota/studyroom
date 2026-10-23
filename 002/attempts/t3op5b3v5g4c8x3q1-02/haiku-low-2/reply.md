Only one value is asked, so each line of the answer is a single value.

**Constraints on y.** Only A1 (writes 1) and C3 (writes 4) write y.
- A4 reads 4, so C3 is the last y-write before A4. Since A1 precedes A4 in program order, A1 must come before C3 or after A4. Its only consistent position with the next constraint is before C3.
- B1 reads 1, so A1 is the last y-write before B1. Together with the above, the order is A1 < B1 < C3 < A4.
- B2 falls after B1. It reads 1 if it happens before C3, and 4 if it happens after C3. So B2 gives v ∈ {1, 4}, and B3 writes v to z.

**Possible values of C4.** C4 comes after C1, so some write to z always precedes it. The candidates for the last z-write before C4 are C1 (writes 2), A2 (writes 1), and B3 (writes v). That gives 1, 2, or 4. Each one is achievable:
- **4:** A1, A2, B1, C1, C2, C3, B2, B3, C4, A3, A4, A5. B2 reads 4, B3 writes 4 to z, and C4 reads 4.
- **1 via B3:** C1, A1, A2, B1, B2, B3, C2, C3, C4, A3, A4, A5. B2 reads 1, B3 writes 1 to z, and C4 reads 1.
- **2:** A1, A2, B1, B2, B3, C1, C2, C3, C4, A3, A4, A5. C4 reads 2 from C1.
- **1 via A2:** C1, A1, B1, B2, B3, A2, C2, C3, C4, A3, A4, A5. C4 reads 1 from A2.

BEGIN
1
2
4
END