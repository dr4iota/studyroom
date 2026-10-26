**Constraints on the order of effects**

1. B5 reads z = 4, and A3 is the only write to z. So A3 takes effect before B5.
2. A2 reads z = 0. A2 comes before A3 in thread A, so this always holds.
3. B1 reads x = 0. The value 3 written by A5 must not be visible yet, so B1 takes effect before A5.

**Stages of x as thread B writes it**

| Stage | When | Value of x (ignoring A5) |
|---|---|---|
| 0 | before B2 | 0 |
| 1 | after B2 | 2 |
| 2 | after B3 | 1 |
| 3 | after B4 | 2 |

**What A1 and A4 can return**

- A1 takes effect before A5, so it sees x at some stage i. A1 can return 0, 2 or 1.
- A4 comes after A1 and before A5. It sees x at some stage j with j ≥ i.

**What the final value of x can be**

- If A5 takes effect after B4, x ends as 3.
- If B4 takes effect after A5, x ends as 2. This needs A4 to be at stage j < 3.
- The order A3 → A4 → A5 → B4 → B5 satisfies every constraint.

**Combining the cases**

- **j = 3 (A4 returns 2):** A5 must come after B4, so x ends as 3. A1 is 0, 2 or 1.
- **j = 0 (A4 returns 0):** A1 must also be at stage 0, so A1 returns 0. x ends as 2 or 3.
- **j = 1 (A4 returns 2):** A1 returns 0 or 2. x ends as 2 or 3.
- **j = 2 (A4 returns 1):** A1 returns 0, 2 or 1. x ends as 2 or 3.

BEGIN
0 0 2
0 0 3
0 2 2
0 2 3
2 2 2
2 2 3
1 2 3
0 1 2
0 1 3
2 1 2
2 1 3
1 1 2
1 1 3
END