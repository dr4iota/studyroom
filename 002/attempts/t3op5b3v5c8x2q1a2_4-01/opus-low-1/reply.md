**Writes to z:**
- Thread A: A4 writes 3.
- Thread B: B1 writes 4, then B2 writes 2, then B3 writes 5, in that order.
- Thread C: C2 writes 1.

**Which write can come last:**
- B1 (4) and B2 (2) can never be the last write to z. B3 always takes effect after them in the same thread.
- There are no known read results or sync points, so nothing constrains the order between threads.
- So A4 (3), B3 (5) or C2 (1) can each be the last write to z. For example, finish the other two threads first, then let that thread finish.

The possible final values of z are therefore 1, 3 and 5.

BEGIN
1
3
5
END