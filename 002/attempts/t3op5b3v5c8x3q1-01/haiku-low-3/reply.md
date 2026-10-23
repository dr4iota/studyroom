**Possible values of B3: 0, 1, and 5.**

- **C2 always returns 5.** C1 (write 5 to x) comes before C2 in program order, and C4 (write 4 to x) comes after it, so C4 can never have taken effect before C2. C5 therefore always writes 5 to y.
- **A3 returns 1, 4, or 5.** A1 always precedes A3, so A3 never sees 0. It can see B4's 4 or C5's 5 if those took effect earlier.
- **B3 cannot return 4.** The only way to get a 4 into y is B4, which comes after B3 in B's program order. The other route, A5 writing A3's value of 4, would require B4 < A3 < A5 < B3, which contradicts B3 < B4.
- **B3 can return 0:** B1–B3 run before A1 and C5.
- **B3 can return 1:** A1 takes effect, then B1–B3 run before any other write to y.
- **B3 can return 5:** C1–C5 run after A1, then B1–B3 run and see C5's 5.

BEGIN
0
1
5
END