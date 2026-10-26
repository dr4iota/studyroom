The outcomes are the 14 triples below. A1 can only see writes from D3, and B3 can only see writes from A3 and D3, so both values are 0 or the value D2 read. Final y is always 0 or 3, and D2's value determines which combinations are possible.

**Key facts**
- C2 reads y, and only D1 can have written before it, so C2 (and therefore C4's written value) is 0 or 3.
- The possible values of D2 and final y pair up as (D2, final y) ∈ {(0,0), (2,0), (2,3), (3,0), (3,3)}. Final y is never 2, because C4 always follows C3.
- A1 is 0 or D2's value, depending on whether D3 precedes it. B3 is also 0 or D2's value. Each of these can be set independently of the others by placing A1, B3, and D3 in the timeline.

**Combinations (A1, B3, final y)**
- Final y = 0: (0,0), (0,2), (2,0), (2,2), (0,3), (3,0), (3,3)
- Final y = 3: (0,0), (0,2), (2,0), (2,2), (0,3), (3,0), (3,3)

BEGIN
0 0 0
0 2 0
2 0 0
2 2 0
0 3 0
3 0 0
3 3 0
0 0 3
0 2 3
2 0 3
2 2 3
0 3 3
3 0 3
3 3 3
END