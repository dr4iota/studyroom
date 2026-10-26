Constraints: A4 must return 5, and A3 (which precedes A4) overwrites y with whatever A2 read from z. The only way y is 5 at A4 is if B1 takes effect between A3 and A4. Since B3 (the only write of 2 to z) comes after B1 in thread B, A2 must read z before B3, so A2 returns 0 and A3 writes 0.

Required order: A1(5) → A2 → A3(0) → B1(5) → A4. C2 is unconstrained relative to these, so it can read 0 (before A1, or between A3 and B1) or 5 (between A1 and A3, or after B1). It can never read 2.

BEGIN
0
5
END