Writes to z: A4 (3), B1 (4), B2 (2), B3 (5), C2 (1). The final value is the last write in the order.

Constraints: B's writes happen in order B1<B2<B3. A4 is after A1-A3, and C2 is after C1. Otherwise, the threads are independent, since the only data dependencies are through x and y, and those do not affect z.

Which values can be last?
- 3 (A4 last): A4 can be placed after everything. Possible.
- 4 (B1 last): B1 must precede B2 and B3, which also write z, so B1 can't be last. Impossible.
- 2 (B2 last): B3 follows B2, so impossible.
- 5 (B3 last): possible.
- 1 (C2 last): possible.

Values 3, 5 and 1 are possible.

BEGIN
1
3
5
END