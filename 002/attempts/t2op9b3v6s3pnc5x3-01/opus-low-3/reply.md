Every execution gives A9 = 5. Final y is 4 or 6, and final z is 4 or 6. Four combinations are possible.

**Ordering constraints**
- In thread B, B1–B5 happen before P. B1–B3 also happen before R. B7–B9 happen after Q.
- In thread A, A7 and A8 happen after P. A1–A8 all happen before Q. A9 happens after R.
- So the order is: B1–B5, then P, then A7 and A8, then Q, then B7–B9.

**Q1: the value returned by A9**
- The writes to x are B2 and B4 (both 1, before P), A8 (5, between P and Q), and B9.
- B8 runs after Q. A8 is the last write to x before Q, so B8 returns 5 and B9 writes 5.
- A9 comes after A8. Whether it takes effect before or after B9, x holds 5.
- A9 always returns 5.

**Value read by A4 (call it v)**
- A4 reads y after A1 writes 5 and A2 writes 4.
- B5 writes 6 to y and can land anywhere relative to A's steps.
- If B5 takes effect between A2 and A4, then v = 6. Otherwise v = 4.

**Q2: the final value of y**
- y is decided by whichever of A6 (writes v) and B5 (writes 6) takes effect last.
- If v = 6, B5 already happened before A4, so A6 is last and y = 6.
- If v = 4, y is 4 when A6 is last, or 6 when B5 comes after A6.

**Q3: the final value of z**
- The writes to z are B1 (2), B3 (6), A3 (1) and A5 (v).
- B3 can take effect after A5, giving z = 6.
- A5 can take effect after B3, giving z = v.

**Combining**
- With v = 4, y and z can each be 4 or 6 independently. For y = 6 and z = 4, B5 comes after A6 and A5 comes after B3, which is allowed.
- With v = 6, both y and z are 6.

BEGIN
5 4 4
5 4 6
5 6 4
5 6 6
END