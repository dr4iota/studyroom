A6 must return 1, and the final value of z can be 3 or 5.

**Step 1: what B3 returned.** C8 reads z = 3. The only writes to z are A1 (2), A2 (5), C6 (1) and B8 (the value B3 read). So B8 must have written 3, which means B3 returned 3. B8 also takes effect before C8, and no other write to z comes between them.

**Step 2: where A2 can fall.** B4 reads z = 2, and A1 is the only write of 2 to z. So A1 takes effect before B4, and A2 takes effect after B4. C6 does not fall between A1 and B4.

**Step 3: Q1, the value returned by A6.** The writes to y are C2 (5), C3 (2), A4 (1) and A8.
- A3 reads y = 2, so C3 takes effect before A3.
- C2 comes before C3 in thread C, so it is also before A3.
- A8 comes after A6 in thread A.

So between A4 and A6, nothing else writes to y. A6 must return 1.

**Step 4: Q2, the final value of z.** Order so far: A1 before B4 before B8 before C8, and C6 before B8. A2 is the only write to z not yet placed relative to B8.
- If A2 takes effect before B8, z ends as 3.
- If A2 takes effect after C8, z ends as 5. C3 can still come before A3, so this order is valid.

A2 cannot fall between B8 and C8, because C8 must still read 3.

**Step 5: check the other conditions.** The final x = 3 can be met, since B7 (which writes 3) can be the last write to x. A7 reading x = 3 is also satisfiable, because x holds 3 after B1, C1, C7 and B5–B7.

BEGIN
1 3
1 5
END