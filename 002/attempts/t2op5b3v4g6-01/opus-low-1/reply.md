No sync points apply, and x is never written, so B2 returning 0 is always consistent and adds no constraint. What matters is the order of the writes to y: A1=3, A3=4, A4=3 by thread A, and B4=1, B5=2 by thread B.

**Possible values on their own**
- **A2** happens after A1 and before A3. It returns 3 if no B write takes effect between A1 and A2. It returns 1 if B4 takes effect there. It returns 2 if B5 takes effect there.
- **B3** happens before B4 and B5. It returns 0 if it comes before A1, 3 if it comes after A1 or after A4, and 4 if it comes between A3 and A4.
- **Final y** is 3 if A4 is the last write, or 2 if B5 is the last write.

**Case A2 = 3:** B4 and B5 both come after A2, and B3 can fall anywhere.
- B3 = 0 when it comes before A1, B3 = 3 when it comes between A1 and A3 or after A4, and B3 = 4 when it comes between A3 and A4.
- For B3 = 0, 3 or 4, B5 can come before or after A4, so the final value can be 2 or 3.
- That gives all 6 combinations.

**Case A2 = 1:** B4 comes between A1 and A2, and B5 comes after A2.
- B3 comes before B4, which is before A3, so B3 is 0 or 3.
- B5 can come before or after A4, so the final value is 3 or 2.
- That gives 4 combinations.

**Case A2 = 2:** B5 comes between A1 and A2.
- A4 must then be the last write, so the final value is 3.
- B3 comes before A2, so it is 0 or 3.
- That gives 2 combinations.

BEGIN
3 0 2
3 0 3
3 3 2
3 3 3
3 4 2
3 4 3
1 0 2
1 0 3
1 3 2
1 3 3
2 0 3
2 3 3
END