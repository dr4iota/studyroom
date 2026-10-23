**What each sync point forces**

- **Thread B:** the "before R" line is above all of B's steps, so it constrains nothing. B2 starts before Q and ends after Q. B4 starts after P.
- **Thread C:** C2 starts before P. C1 through C4 all happen before Q, so C4 ends before Q.
- **Thread A:** A3 ends after R. Its start is not constrained.

**Block y**

- The only writes to y are A1 and B3, and both write 1.
- C1 returned 0, so C1 takes effect before both A1 and B3. Nothing prevents this.
- A3 and B4 returned 1, which any later point allows.
- D3 can return 0 (if it comes before A1 and B3) or 1 (if it comes after either).

**Final value of x**

- The last write to x must be the last of B1, C4 or D4. C2 and C3 come before C4, and D1 and D2 come before D4.
- Any of these three can come last, so the final x is 2 (B1 or C4) or 1 (D4).

**A2 and how it links to D3**

- A2 comes after A1 but is otherwise free, so it can return 0, 1, 2 or 3.
- If D3 returns 0, the order is D1 < D2 < D3 < A1 < A2. A2 then comes after D2's write of 1, so it cannot return 0. It can still return 1 (from D2 or D4), 2 (from B1, C2 or C4 placed later) or 3 (from C3 placed later).
- If A2 returns 0, D1 must come after A2, so D3 comes after A1 and returns 1.
- Every other combination can be built, and each one works with either final value.

That excludes only the two combinations with A2 = 0 and D3 = 0, leaving 14.

BEGIN
0 1 1
0 1 2
1 0 1
1 0 2
1 1 1
1 1 2
2 0 1
2 0 2
2 1 1
2 1 2
3 0 1
3 0 2
3 1 1
3 1 2
END