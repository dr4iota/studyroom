Each triple below is written as B2, C1, final x. The writes available are A's values (1, 3, 1, 2, in that order), B3 (writes B2's value) and C2 and C3 (write C1's value). B1 reading 1 means A1 has already taken effect before B1.

**Which (B2, C1) pairs are possible**
- C1 = 0: C1 takes effect before A1. B2 can be 0, 1, 2 or 3. B2 = 0 needs C2 to write 0 after B1 and before B2.
- C1 = 1, 2 or 3: B2 cannot be 0, because A1 happened before B1 and the only other writers of 0 are C2 and C3, which write C1's nonzero value. B2 can be 1, 2 or 3.

**Which final values are possible**
The final value is the last write overall. Three writers can be last:
- A4 can be last, giving 2.
- C3 can be last after A4, giving C1's value.
- B3 can be last after A4, giving B2's value.

A1, A2 and A3 can never be last, since A4 always follows them. So the final value is always 2, C1, or B2.

Taking those three candidates for each feasible (B2, C1) pair gives the list below. Each candidate is also achievable for its pair, because the B and C writes can be placed early or late as needed.

BEGIN
0 0 0
0 0 2
1 0 0
1 0 1
1 0 2
2 0 0
2 0 2
3 0 0
3 0 2
3 0 3
1 1 1
1 1 2
2 1 1
2 1 2
3 1 1
3 1 2
3 1 3
1 2 1
1 2 2
2 2 2
3 2 2
3 2 3
1 3 1
1 3 2
1 3 3
2 3 2
2 3 3
3 3 2
3 3 3
END