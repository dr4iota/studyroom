Since A1 cannot be 4 and B3 cannot be 0 is never forced, all 12 combinations are possible.

**Constraints.** There are no sync points, so any interleaving that keeps each thread's order is allowed. The only known result is that B1 returned 0. This holds automatically, because B1 comes before B2, which is the only write to y. So the one real requirement is that each thread keeps its order.

**Q1, the value A1 returns.**
- If A1 takes effect before B2, it returns 0.
- If A1 takes effect after B2, it returns 4.

**Q2, the value B3 returns.** B3 reads x after B2. A's writes to x happen in the order A2(2), A3(4), A5(2). So B3 can return:
- 0, if B3 is before A2;
- 2, if B3 is between A2 and A3, or after A5;
- 4, if B3 is between A3 and A5.

**Q3, the final value of x.** It is set by whichever of A5(2) and B5(4) takes effect last, so it is 2 or 4.

**Checking that every combination works.** The hardest case is A1 = 4, since then A1 and all of A2 to A5 come after B2.
- B3 = 0: B3 comes right after B2, before A2. B5 can then go before or after A5, giving a final x of 2 or 4.
- B3 = 2: B3 goes between A2 and A3. B5 can go before or after A5, giving 2 or 4.
- B3 = 4: B3 goes between A3 and A5. B5 can go before or after A5, giving 2 or 4.

When A1 = 0, A1 simply goes before B2, and the rest of the schedule can be the same as above. So all 2 × 3 × 2 = 12 combinations are possible.

BEGIN
0 0 2
0 0 4
0 2 2
0 2 4
0 4 2
0 4 4
4 0 2
4 0 4
4 2 2
4 2 4
4 4 2
4 4 4
END