**Constraints that matter**

- Every step of thread B happens before Q, and A2–A8 happen after Q. So all of B (B1–B8) finishes before A2 starts.
- A1 is above the "after Q" line, so it can take effect anywhere before A2, including in the middle of B's operations.
- The lines for P, R and S add nothing new, because all of B already comes before A2–A8.

**Thread B**

- B1 and B2 read x = 0. Thread A does not write x until A5, which comes after all of B.
- B3 reads y. It returns 1 if A1 took effect before B3, and 0 otherwise.
- B4 writes 6 to z.
- B5 writes B3's value to x.
- B6 writes 0 (B2's value) to y.
- B7 writes 6 to y.
- B8 reads y. It returns 6, unless A1 takes effect between B7 and B8, in which case it returns 1.

**Thread A after Q**

- A2 reads x, which holds B3's value (from B5).
- A3 writes 2 to z. That overwrites B4's 6, so A7 returns 2.
- A4 writes A2's value to y, so A8 returns B3's value.

**Where A1 can take effect**

| Position of A1 | B3 | A8 | B8 |
|---|---|---|---|
| Before B3 | 1 | 1 | 6 |
| Between B3 and B7 | 0 | 0 | 6 |
| Between B7 and B8 | 0 | 0 | 1 |
| After B8 | 0 | 0 | 6 |

In every case A7 returns 2, which gives three distinct combinations.

BEGIN
2 1 6
2 0 6
2 0 1
END