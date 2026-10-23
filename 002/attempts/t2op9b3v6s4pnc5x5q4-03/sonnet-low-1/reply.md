Two facts about the ordering decide everything.

**B2 always reads 0.** B1–B3 end before R, and B4 ends before P. All of A's writes to x come after P, and B5 comes after B4. So nothing has written x when B2 reads it, and B9 always writes 0 to y.

**Let v be the value A2 reads from y.** The writes to y are B1 (6), B8 (6) and B9 (0). B8 and B9 come after B5, which comes after B4, which is before Q and so before A2. Those writes are free to land before or after A2, so v is 6 or 0.

- A3 writes v to z after P, and B4's write of 3 to z is before P. So the final z equals v (Q4 = v).
- A6 writes v to x, and A8 is after A6 in thread order.

**Case v = 0.** A2 can only read 0 if B9 has already happened. B9 is after B5, so B5 is before A2 and therefore before A6.
- A6 then overwrites B5's write of 4, so A8 = 0.
- B9 is B's last write to y, so A9 = 0.
- Nothing writes x after A8, so the final x is 0, and z is 0.
- This gives the combination 0 0 0 0.

**Case v = 6.**
- B5 must end before S, and S is before A8. B5 is either before A6 or between A6 and A8.
- If B5 is before A6, A8 = 6. If B5 is after A6, A8 = 4. Nothing writes x after A8, so the final x equals A8.
- A9 reads y after B5 has happened. It reads 6 if B9 hasn't happened yet (B1 or B8 supplied the 6), and 0 if B9 has. Either is possible with either value of A8.
- z is 6.
- This gives A8 ∈ {6, 4} and A9 ∈ {6, 0}, all four combinations.

BEGIN
0 0 0 0
6 6 6 6
6 0 6 6
4 6 4 6
4 0 4 6
END