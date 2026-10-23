The possible outcomes are **(0, 1, 1, 0)**, **(0, 4, 1, 0)** and **(1, 4, 1, 1)**.

**Key facts from the constraints:**

- **A4 always reads 1.** B1 (writes z=1) precedes P, which precedes A3, which precedes A4. A1 (z=6) is overwritten by B1 before A4.
- **A7 always reads 1.** A9 precedes R, which precedes B8, so A9 is before B8. Since A7 is before A9, B8 can't be visible to A7, and A6 (which writes 1) is the last z-write before A7.
- **A8 always writes y=1**, so the final y is always 1 (Q3).
- **B9 reads B8's value, and B8 is the last z-write.** B8 comes after A9, R, and every other z-write, so B9 = final z = B2's value, call it v (Q1 = Q4 = v).
- **v is 0 or 1.** B2 reads y, which only A8 writes (value 1). So v = 1 exactly when A8 takes effect before B2, and v = 0 otherwise.
- **Final x is 1 or 4.** B7 (writes 4) is the last B-write to x, and A2 (writes 1) is the only other x-write that can come last. A2 comes after B7 for final x=1, and before B7 for final x=4.

**Feasibility:**

- **v=1, x=1 is impossible.** It needs A8 before B2 and A2 after B7. But B2 precedes B7 in B's program order, and A2 precedes A8 in A's program order, so B2 < B7 < A2 < A8, which contradicts A8 < B2.
- **v=0, x=1** is achievable: B1, A1, S, B2, B3–B7, P, A2–A8, Q, A9, R, B8, B9.
- **v=0, x=4** is achievable: B1, A1, S, P, A2–A7, B2–B7, Q, A8, A9, R, B8, B9.
- **v=1, x=4** is achievable: B1, A1, S, P, A2–A8, B2–B7, Q, A9, R, B8, B9.

Each combination is listed as Q1 Q2 Q3 Q4.

BEGIN
0 1 1 0
0 4 1 0
1 4 1 1
END