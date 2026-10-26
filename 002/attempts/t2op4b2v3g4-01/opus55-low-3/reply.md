A2 and A3 can only see B's writes, in B's order. The final value is 1 or 2, depending on whether B4 or A4 takes effect last.

**What the known results force**
- Nothing ever writes y, so A1 returning 0 is always true and adds no constraint.
- B1 is B's first operation. It returns 0, so no write to x took effect before it. A's only write is A4, so A4 takes effect after B1.
- A4 is A's last operation, so it takes effect after A2 and A3. That means A2 and A3 never see A's own 2.

**Values seen by A2 and A3**
B's writes take effect in order: 3, then 2, then 1. So x goes through 0, 3, 2, 1. A2 comes before A3, so A3 sees the same value as A2 or a later one in that sequence. That gives 10 pairs:
(0,0), (0,3), (0,2), (0,1), (3,3), (3,2), (3,1), (2,2), (2,1), (1,1).

**Final value of x**
The final value is 1 if B4 (write 1) is the last write, or 2 if A4 (write 2) is.
- If A3 returned 1, B4 had already taken effect before A3. A4 comes after A3, so A4 is last and x ends at 2.
- In every other case, A4 can take effect either before or after B4, so x can end at 1 or 2.

BEGIN
0 0 1
0 0 2
0 3 1
0 3 2
0 2 1
0 2 2
0 1 2
3 3 1
3 3 2
3 2 1
3 2 2
3 1 2
2 2 1
2 2 2
2 1 2
1 1 2
END