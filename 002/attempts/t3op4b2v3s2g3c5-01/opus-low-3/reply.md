**Constraints from the sync points**

- **Thread A:** All of A1–A3 finish before P.
- **Thread B:**
  - B3 ends after P, so its effect can fall before P.
  - B4 ends after Q. Thread C finishes before Q, so B4's effect can come after every write by C.
- **Thread C:** All of C1–C4 finish before Q.

**B2's value.** B2 always reads y after B1, so B2 returns 1 or 2. It returns 2 if C2 or C4 takes effect between B1 and B2; otherwise it returns 1. B3 and B4 both write that same value to x.

**A3 must read 2.** C1 or C3 can always take effect after any B3 write and before A3. So this condition never rules out a combination.

**Case A1 = 0.** No write to x has taken effect before A1. A2 can return 0, 1 or 2, independently of whether B2 returns 1 or 2. For example, A2 can read 0 early, while C2 later feeds B2 the value 2. All 6 combinations are possible.

**Case A1 = 2.** C1 (or C3, or B3 writing 2) takes effect before A1. Again A2 can be 0, 1 or 2, and B2 can be 1 or 2, in every combination. All 6 combinations are possible.

**Case A1 = 1.** The only write of 1 to x is B3, so B2 must have returned 1. The order is then B1 → B2 → B3 → A1 → A2.
- A2 cannot return 0, because B1 already wrote 1 to y.
- A2 can return 1 (no C write to y yet).
- A2 can return 2 (C2 takes effect after B2 and before A2).
- C1 or C3 then takes effect before A3, so A3 still reads 2.

This gives (1,1,1) and (1,2,1).

That is 14 combinations in total.

BEGIN
0 0 1
0 0 2
0 1 1
0 1 2
0 2 1
0 2 2
2 0 1
2 0 2
2 1 1
2 1 2
2 2 1
2 2 2
1 1 1
1 2 1
END