B4 can return 5 or 3.

**Constraints from the known end state.** y ends at 0, but A1 and C1 both write 3 to y. So the last write to y must be B2 writing 0, which means:
- B1 read y = 0, so it took effect before A1 and C1.
- B2 took effect after both A1 and C1.

**Constraints from x.** x ends at 3, and C2 writes 5. So the last write to x must be C5, and it must write 3. That means C3 read y = 3.
- C3 read 3, so it took effect after C1 and before B2, because B2 would overwrite y with 0.
- This gives the order C1 < C3 < B2, and since C2 precedes C3, also C2 < C3.

**B4's value.**
- B4 comes after B2, which comes after C3, which comes after C2. So x is already 5 when B4 runs, and it can't be 0.
- C5 comes after C3, so it may fall before or after B4.
  - If C5 takes effect before B4, B4 reads 3.
  - If C5 takes effect after B4, B4 reads 5.

Thread A's reads don't constrain anything, so both values are possible.

BEGIN
3
5
END