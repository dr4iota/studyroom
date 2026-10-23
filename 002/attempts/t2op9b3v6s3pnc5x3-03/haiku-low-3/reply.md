The final value of z is always the value B2 reads, and the possible outcomes are these five (Q1 Q2 Q3):

- **Q3:** B9 always takes effect after every other write to z, so the final z equals B2's result. B2 can only see 0 (before A3) or 5 (from A3, or from A9 when A6 = 5). It can never see 3, because seeing 3 would require B2 to come after A9, which in turn requires B3 to come before A6, but B2 comes before B3.
- **Q1:** A1 sees 3 only if B3 precedes it, and then B2 precedes B3 and sees 0. Otherwise A1 sees 0.
- **Q2:** A5 reads 5 only if B1 lands between A4 and A5, which forces B2 to be 5. Otherwise A5 returns A2's value, which is 0 or 3.

The consistent triples are (A1, A5, B2) = (0,0,0), (0,0,5), (0,3,0), (0,5,5), and (3,3,0). Each has a timing witness, for example (3,3,0) with B1, B2, B3 all before A1.

BEGIN
0 0 0
0 0 5
0 3 0
0 5 5
3 3 0
END