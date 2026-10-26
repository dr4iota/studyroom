Two values are possible for A6 and z together: A6 always returns 1, and z ends as 3 or 5.

**A6.** A3 reads y = 2, and the only write of 2 to y is C3, so C3 takes effect before A3. C2 (value 5) comes before C3 in thread C, so it is overwritten by then. A4 writes 1 after A3, and A6 comes after A4. Neither C2 nor C3 can fall between A4 and A6. A8 comes after A6, so it cannot affect it. A6 therefore always returns 1.

**z.** The writes to z are A1 (2), A2 (5), C6 (1) and B8 (the value B3 read).
- C8 reads 3, and the only write that can put 3 in z is B8. So B8 takes effect before C8, and B3 must have read 3 from x.
- B4 reads 2, so A1 is the last write to z before B4. B8 comes after B4, and A2 cannot fall between A1 and B4.
- C6 comes before C8 in thread C. Since C8 reads 3, C6 must take effect before B8, otherwise it would overwrite the 3.
- A2 can take effect after B4 and before B8, in which case B8 overwrites it and z ends as 3.
- A2 can instead take effect after C8, in which case z ends as 5.
- A2 cannot fall between B8 and C8, because C8 would not read 3.

The other constraints can all be met in either case. A7 and B2 read 3, and C7 writes 3 last to x while B5–B7 also write 3, so the final x = 3. Both z = 3 and z = 5 are therefore achievable.

BEGIN
1 3
1 5
END