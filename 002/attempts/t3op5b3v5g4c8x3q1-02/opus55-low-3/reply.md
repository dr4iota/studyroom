The possible values for C4 are **1, 2 and 4**. Each is shown possible by an example ordering below, and no other value can occur.

**Constraints from the known results**

- The writes to y are A1 (writes 1) and C3 (writes 4).
- B1 returned 1, so B1 takes effect after A1 and before C3.
- A4 returned 4, so A4 takes effect after C3.
- B2 can therefore return 1 or 4, so B3 writes 1 or 4 to z.
- The writes to z are A2 (writes 1), C1 (writes 2) and B3 (writes 1 or 4).
- C4 reads z after C1, so the only candidate values are 1, 2 and 4.

**Each candidate is reachable**

| C4 value | Example order of effects | Why C4 sees that value |
|---|---|---|
| 2 | A1, A2, B1, B2 (reads 1), B3, C1, C2, C3, C4 | C1 is the last write to z before C4. |
| 1 | A1, B1, C1, A2, C2, C3, C4 | A2 is the last write to z before C4. |
| 4 | A1, B1, C1, C2, C3, B2 (reads 4), B3, C4 | B3 writes 4 and is the last write to z before C4. |

The remaining operations can be placed after C4, and these orders agree with every known result.

BEGIN
1
2
4
END