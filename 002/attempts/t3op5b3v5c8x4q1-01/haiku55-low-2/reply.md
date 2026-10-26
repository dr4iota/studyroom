Only one value is possible for C4: **2**.

- **Why 4 is impossible:** C4 can read 4 only if B3 is the last write to y before C4. Then B4 (which must read 2) needs a 2-write after B3, and the only candidate is A2 writing a1 = 2. But that A2 would have to fall after C4, and A3 would then come after A2, so A3 could not feed z before C3. This contradicts C3 reading z = 2.
- **Why 0 is impossible:** C4 can read 0 only if A2 writes 0 and is the last write before C4. Then A3 runs after A2 and sees no 2 (any 2-write, C2, must precede C4 and so precede A2), so z never receives 2 and C3 cannot read 2.
- **Why 2 is possible:** Take this order: B1, B2, B3 (y = 4); C1; C2 (y = 2); B4 reads 2; A1 reads 2; A2 writes 2 to y; A3 reads 2; A4 writes 2 to z; C3 reads z = 2; C4 reads y = 2. Every stated result holds.

BEGIN
2
END