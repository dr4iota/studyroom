Listed below are all 21 combinations.

**What can be written**
- **To z:** B1 writes 1, C1 writes 2, and A2 and A3 both write a. Here a is the value A1 read, so a can be 0, 1 or 2.
- **To x:** only C2 writes, and it writes 1. So B2 returns b = 0 or 1.
- **To y:** A4 writes a and B3 writes b. The final y is whichever of the two takes effect last.

There are no sync points, so any interleaving that keeps each thread's order is allowed.

**What each final y needs**
- **y = 0:** either a = 0 with A4 last, or b = 0 with B3 last.
- **y = 1:** either a = 1 with A4 last, or b = 1 with B3 last. b = 1 means B2 runs after C2.
- **y = 2:** a = 2 with A4 last.

**When B5 or C4 returns 0**
- B5 comes after B1, and C4 comes after C1. A 0 in z after that point can only come from A2 or A3 with a = 0.
- So if either read returns 0, a = 0 and y can only be 0 or 1.
- Every pair (B5, C4) that contains a 0 is reachable. For example:
  - **(0,1):** A1, C1, B1, C4, A3, B5.
  - **(2,0):** B1, C1, B5, A3, C4.
  - The other pairs with a 0 are built in the same way.

**(1,1), (2,2) and (1,2)**
- All three are reachable with y = 0, 1 or 2.
- Example for (1,1) with y = 2: C1, A1, A2, A3, B1, B5, C4, A4.
- Example for (2,2) with y = 1: B1, A1, A2, A3, C1, B5, C4, A4.
- Example for (1,2) with y = 2: C1, A1, A2, A3, C4, B1, B5, A4.
- y = 0 is reachable for each by taking a = 0, or b = 0 with B3 last.

**(2,1)**
- **a = 0:** B5 = 2 needs B1, then C1, then B5, with no later write of 1 before B5. C4 = 1 needs C1, then B1, then C4. These two orders contradict each other.
- **a = 2:** the 1 that C4 sees must come from B1, written after C1 and after A3. Then B5, which comes after B1, has no 2 written after B1 to read. This is impossible.
- **a = 1:** the order B1, A1, A2, C1, B5, A3, C4 works.
  - B3 comes before B5, which is before A3 and A4, so B3 cannot be the last write to y.
  - A4 is therefore last and writes a = 1, so y = 1 only.

BEGIN
0 0 0
0 0 1
0 1 0
0 1 1
0 2 0
0 2 1
1 0 0
1 0 1
2 0 0
2 0 1
1 1 0
1 1 1
1 1 2
1 2 0
1 2 1
1 2 2
2 2 0
2 2 1
2 2 2
2 1 1
END