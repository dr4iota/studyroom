Every combination of the six possible A3/A4 pairs with a final x of 2 or 4 is possible, giving 12 outcomes. No sync points appear in this problem, so only the known read results limit the orderings.

**Constraints from known results**
- A1 reads x = 0, so A1 takes effect before B1, which is the first write to x.
- B2 reads x = 2, so A5 (write 4 to x) cannot take effect between B1 and B2.
- A5 comes after A1, so A5 is either before B1 or after B2.
- A2 reads z = 0. Nothing writes z, so this adds no constraint.

**Values A3 and A4 can return**
- B writes y = 1 (B3) and then y = 3 (B4).
- A3 takes effect before A4, so A4's value can never be older than A3's.
- The possible pairs are (0,0), (0,1), (0,3), (1,1), (1,3) and (3,3).

**Final value of x**
- If A5 is before B1, the final x is 2. In this case A3 and A4 are also before B1, so both read 0.
- If A5 is after B2, it can take effect before B5 (final x is 2) or after B5 (final x is 4).
- A5 only needs to follow A4, and A4 can take effect at any point after B4. So A5 can fit between B4 and B5, or after B5, whichever y pair A3 and A4 returned.

Therefore every y pair can occur with a final x of either 2 or 4.

BEGIN
0 0 2
0 0 4
0 1 2
0 1 4
0 3 2
0 3 4
1 1 2
1 1 4
1 3 2
1 3 4
3 3 2
3 3 4
END