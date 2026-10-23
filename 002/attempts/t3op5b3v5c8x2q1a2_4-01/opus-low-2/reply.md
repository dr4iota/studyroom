Final z is whichever write to z takes effect last, so I look at each thread's last write to z.

**Writes to z:**
- Thread A: A4 writes 3.
- Thread B: B1 writes 4, B2 writes 2, B3 writes 5, in that order.
- Thread C: C2 writes 1.

There are no sync points and no known read results. So any interleaving that keeps each thread's own order is allowed. Values read from y and x never affect z.

**Which writes can be last:**
- A4 (3) can be last. Run A4 after all of B and C finish.
- B3 (5) can be last. Run it after A4 and C2.
- C2 (1) can be last. Run it after A4 and B3.
- B1 (4) and B2 (2) can never be last, because B3 always follows them in thread B.

So the final value of z can be 1, 3 or 5.

BEGIN
1
3
5
END