**Constraints from the sync points**

- A1–A3 happen before Q, and B2 onward happens after Q. So A2 and A3 come before B2, B3 and B4.
- B1–B4 happen before R, and A4 onward happens after R. So B4 comes before A4.
- B1–B6 happen before P, and A9 happens after P. So B6 comes before A9.

**What A3 returns**

The only writes to z are A1 (1), B4 and B8. B4 and B8 both come after A3, so A3 reads the value from A1. A3 = 1.

**Q1: what A7 returns**

- A4, A5 and A6 write 1, 6 and 1 to z. B4 comes before A4, so it never affects A7.
- If B8 (writes 3 to z) takes effect between A6 and A7, then A7 = 3.
- Otherwise A7 reads the value from A6, so A7 = 1.

**Case A7 = 3**

- B8 comes before A7, so the order is B6 < B7 < B8 < A7 < A8 < A9.
- B6 cannot see A8, so B6 reads 3 from B3.
- B7 comes before A9, so final x = 1 (from A9).
- B8 is the last write to z, so final z = 3.
- Result: 3 3 1 3.

**Case A7 = 1**

- **B6 = 1:** A8 comes before B6. Then B7 and B8 come after A7, so final z = 3. B7 can take effect before or after A9, so final x is 1 or 5.
  - Results: 1 1 1 3 and 1 1 5 3.
- **B6 = 3:** B8 can come before A6 (final z = 1) or after A7 (final z = 3).
  - If final z = 1, B7 comes before B8, which comes before A6 and therefore before A9. So final x = 1.
  - If final z = 3, B7 can come before or after A9, so final x is 1 or 5.
  - Results: 1 3 1 1, 1 3 1 3 and 1 3 5 3.

BEGIN
3 3 1 3
1 1 1 3
1 1 5 3
1 3 1 1
1 3 1 3
1 3 5 3
END