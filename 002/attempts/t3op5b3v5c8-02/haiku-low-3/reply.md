The possible outcomes are below. Since `y` is written only once, by B4, every read of `y` returns 0 before B4 and the value B3 read (`b3`) after it. Since B3 always follows B2, `b3` is 2 when C1 falls between B2 and B3, and 4 otherwise. C2 is always followed by C4, so the final `x` is 3 (B1 last), the value A4 wrote, or the value C4 wrote. Enumerating the orderings consistent with these constraints gives 14 outcomes.

BEGIN
0 0 0
0 0 3
4 0 0
0 4 0
4 4 0
0 4 4
4 4 4
4 0 4
2 0 0
2 0 2
0 2 0
0 2 2
2 2 0
2 2 2
END