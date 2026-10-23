The possible outcomes are five, listed below in the order Q1 (A5), Q2 (A6), Q3 (A8), Q4 (final y).

**Key facts**

- **B2 always reads 0.** The only write to y that could precede B2 is A4, but A4 comes after A1, which comes after Q, and Q comes after B8, which comes after B2.
- **A1 reads 0.** The y-writes before A1 are B4 (3) and then B8 (0), so the last one is 0.
- **B8 writes 0 to y and B9 writes 0 to x**, since b2 = 0.
- **Final y equals A3's value.** A4 is the last write to y, because it comes after A1, which comes after all of B's writes to y. A4 writes A3's value, so final y = a3.
- **x's writes are B1 (2), B3 (4), B9 (0).** B1 and B3 always precede A3 and the A5–A8 reads, since they precede B8, which precedes Q and P. So x is 4 from B3 onward until B9 takes it to 0. A3 and the reads A5, A6, A8 occur in that order, so their values form a pattern of 4s followed by 0s, determined by where B9 falls.
- **Each placement of B9 is achievable.** B9 only has to come after B8, and nothing else constrains it relative to the A-thread operations, so all five split points can occur.

**Cases by where B9 falls**

1. Before A3: a3 = 0, so A5 = A6 = A8 = 0 and y = 0.
2. After A3 but before A5: a3 = 4, so A5 = A6 = A8 = 0 and y = 4.
3. Between A5 and A6: a3 = 4, A5 = 4, A6 = A8 = 0, and y = 4.
4. Between A6 and A8: a3 = 4, A5 = A6 = 4, A8 = 0, and y = 4.
5. After A8: all reads are 4 and y = 4.

BEGIN
0 0 0 0
0 0 0 4
4 0 0 4
4 4 0 4
4 4 4 4
END