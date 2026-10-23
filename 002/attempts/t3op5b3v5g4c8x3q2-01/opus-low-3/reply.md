**Possible combinations:** (0, 0), (1, 0), (1, 1). The pair (0, 1) is impossible.

**Step 1: the value of y never changes.** The only write to y is A2, which writes back what A1 read from y. Before A2 there is no write to y, so A1 reads 0. A2 therefore writes 0, and y stays 0 throughout. B3 reading 0 is consistent with every ordering.

**Step 2: what A4 writes to x.** A4 writes A1's value, which is 0. So x receives two writes: 1 from B1 and 0 from A4. There are no sync points, so these can occur in either order.

**Step 3: C4 always takes effect after B1.**
- C2 reads 3, so it takes effect after a write of 3 to z, which is B2 or B4.
- B1 takes effect before B2, which comes before B4.
- C4 follows C2 in thread C.
- So the order is B1 → B2 → C2 → C4.

**Step 4: the possible combinations.**
- **C4 = 0:** C4 comes after B1, so it can only read 0 if A4 took effect after B1 and before C4. A4 is then the last write to x, so x ends as 0. This gives (0, 0), and (0, 1) cannot happen.
- **C4 = 1:** C4 comes after B1 and before A4, or A4 comes before B1.
  - If A4 comes after C4, x ends as 0, giving (1, 0).
  - If A4 comes before B1, x ends as 1, giving (1, 1).

Each case is realisable. For example, the order C1, B1, B2, C2, C3, B3, B4, then all of thread A, then C4 gives (0, 0). Moving C4 before A4 gives (1, 0). Running thread A entirely before B1 gives (1, 1).

BEGIN
0 0
1 0
1 1
END