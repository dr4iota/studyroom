**Reasoning:**

- B1 reads y. The only write to y is B3, which comes after B1 in thread B, so B1 must return 0. Hence B2 writes 0 to z.
- B4 reads z = 4, so C2 (write 4) took effect before B4 with no other z-write in between.
- B2 precedes B3 precedes B4 in thread order, so B2 must take effect before C2 — B2 can never be the last write to z.
- C1 always precedes C2, so C1 can't be last either.
- A1 (write 2) is unconstrained: it can come before C2 (final z = 4) or after B4 (final z = 2).

BEGIN
2
4
END