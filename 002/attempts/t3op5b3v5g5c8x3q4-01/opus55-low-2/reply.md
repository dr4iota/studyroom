Every outcome has y = 3 and z equal to the value C4 read. C4 can read 0, 1, 2 or 3, which gives four combinations.

**Fixed ordering from the known read results**
- B1 read x as 0, so B1 took effect before A1.
- A3 read y as 3, so B2 took effect before A3.
- C2 read z as 3, so C1 took effect before B3, and B3 was the last write to z before C2. C3 comes after C2 in thread C's own order.

**Q2: final value of y.** B2 is the only write to y, so y always ends as 3.

**Q3: final value of z.** The writes to z are C1, B3, C3 and C5. From the ordering above, C1 and B3 both come before C2, which comes before C3, which comes before C5. So C5 is always the last write to z, and z ends equal to the value C4 read.

**Q1: value returned by C4.** C4 comes after C2, so it comes after B3. Each possible value can occur:
- **0:** C4 takes effect before A1, in the order C1, B1, B2, B3, C2, C3, C4, A1. Alternatively, A2 reads y as 0 before B2, and C4 reads x after A4 writes 0 and before B5.
- **2:** C4 takes effect after A1 and before A4 and B5.
- **3:** A2 reads y as 3 after B2, and C4 takes effect after A4 and before B5.
- **1:** C4 takes effect after B5 and before A4. A4 is not constrained relative to B5 and C4, so it can come last.

BEGIN
0 3 0
1 3 1
2 3 2
3 3 3
END