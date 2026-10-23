Only two final values of y are possible: 2 and 5.

**Forced facts:**
- z is written only by A1 (value 5), so B2 and C2 reading 5 means A1 precedes them. B3 comes after B2, so B3 also reads 5. B4 therefore writes 5 to y.
- A2 reads y=1, so C1 is the last y-write before A2. A3 reads y=4, so C4 is the last y-write before A3. Since C4 follows C1 in thread C, C4 must come after A2, giving C1 < A2 < C4 < A3 < A4.
- B4 (writing 5) cannot fall between C1 and A2, or between C4 and A3.
- C4 always precedes A4, and C1 always precedes C4, so the final y is either A4's 2 or B4's 5.

**Both are achievable:**
- **Final y = 2:** A1, B1, B2, B3, B4, C1, C2, C3, A2, C4, A3, A4, B5. Here C3 reads x=1 and A2 reads y=1, and A4 is the last y-write.
- **Final y = 5:** A1, B1, B2, B3, C1, C2, C3, A2, C4, A3, A4, B4, B5. Here B4 is the last y-write.

BEGIN
2
5
END