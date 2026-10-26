Neither thread has sync points, so any interleaving that respects each thread's own order is allowed. The writes to x are B1 (1), A3 (2), A4 (3) and B4 (1).

**Q1 (A1):** A1 comes before A3 and A4, so only B1 can have written before it. A1 is therefore 0 (before B1) or 1 (after B1).

**Q2 (B3):** B3 comes after B1 and before B4, so it cannot be 0. Its value depends on which A writes land before it:
- 1 if neither A3 nor A4 has taken effect.
- 2 if A3 has taken effect but A4 has not.
- 3 if A4 has taken effect, which forces A3 to have as well.

**Q3 (B5):** B5 comes after B4, so it cannot be 0. It is 1 if no A write follows B4, 2 if only A3 follows B4, and 3 if A4 follows B4.

**Combinations of (B3, B5):**
- B3=1: A3 and A4 both come after B3. B5 can be 1, 2 or 3.
- B3=2: A3 comes before B3, and B4 comes after B3. B5=2 would need A3 after B4, which contradicts this, so B5 is 1 or 3.
- B3=3: A3 and A4 both come before B3, and B4 then overwrites with 1. B5 can only be 1.

Each of these pairs works with A1=0 or A1=1. A1=0 puts A1 before B1, and A1=1 puts it after B1 and before A3.

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