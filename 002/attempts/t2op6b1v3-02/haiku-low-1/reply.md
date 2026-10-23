The three asked values are Q1 (B1's read), Q2 (B4's read), and Q3 (final x). Only the writes matter, since no write uses a read's result. Let p_i be the number of A operations finished before B_i takes effect. Then p1 ≤ p2 ≤ … ≤ p5, and any such sequence is a valid interleaving.

- **Q1:** The value is the last A write among A1..A_{p1}. A3 writes 2, A4 writes 3, A5 writes 2, so Q1 = 0 if p1 ≤ 2, 2 if p1 = 3 or 5, and 3 if p1 = 4.
- **Q2:** B3 writes 1. If no A write falls between B3 and B4, Q2 = 1. Otherwise Q2 is the value of the last A write in that window, so 2, 3, or 2 for A3, A4, or A5 respectively. Q2 can never be 0.
- **Q3:** B5 writes 1 and A5 writes 2, and whichever comes later wins. Q3 = 1 if p5 = 5 and 2 otherwise.

Going through the monotone sequences case by case:

- **Q1 = 0** (take p1 = 0): all six (Q2, Q3) pairs with Q2 ∈ {1,2,3} and Q3 ∈ {1,2} are reachable.
- **Q1 = 2**: (2,2,2) is impossible. Getting Q2 = 2 with Q3 = 2 would need p4 = 3, which forces p3 < 3 and contradicts p1 = 3, or p4 = 5, which forces p5 = 5. The other five pairs are reachable.
- **Q1 = 3** (needs p3 ≥ 4): (3,2,2) and (3,3,·) are impossible, because Q2 = 2 with Q3 = 2 and Q2 = 3 both need p3 < p4 with the window containing a write that is too early. The other three pairs are reachable.

That gives 6 + 5 + 3 = 14 combinations.

BEGIN
0 1 1
0 1 2
0 2 1
0 2 2
0 3 1
0 3 2
2 1 1
2 1 2
2 2 1
2 3 1
2 3 2
3 1 1
3 1 2
3 2 1
END