Thread A's writes to x occur in the order 1, 1, 2, 3. Let v1 and v2 be the values read by B1 and B2.

**Constraints on B1 and B2.** B1 and B2 both take effect before B3 and B5, so only A's writes can affect them. Their values therefore never decrease along the sequence 0, 1, 2, 3, which gives v1 ≤ v2. Any such pair is achievable.

**Constraints on B4 and the final value.** B3 and B5 both write v2.
- The final value is 3 if A4 takes effect after B5. Otherwise B5 is last and the final value is v2.
- B4 reads one of A's values, or v2 if B3's write is still the latest.
- If B4 returns 3, A4 came before B4 and so before B5, so the final value is v2.

**Cases by v2.**
- v2 = 0 (so v1 = 0). B3 can overwrite A's writes with 0, so B4 can read 0, 1, 2 or 3. The pairs (B4, final) are (0,0), (0,3), (1,0), (1,3), (2,0), (2,3), (3,0).
- v2 = 1 (v1 is 0 or 1). B4 can read 1, 2 or 3. The pairs are (1,1), (1,3), (2,1), (2,3), (3,1).
- v2 = 2 (v1 is 0, 1 or 2). B4 can read 2 or 3. The pairs are (2,2), (2,3), (3,2).
- v2 = 3 (v1 is 0, 1, 2 or 3). B4 reads 3 and the final value is 3. The pair is (3,3).

BEGIN
0 0 0
0 0 3
0 1 0
0 1 3
0 2 0
0 2 3
0 3 0
0 1 1
0 2 1
0 3 1
0 2 2
0 3 2
0 3 3
1 1 1
1 1 3
1 2 1
1 2 3
1 3 1
1 2 2
1 3 2
1 3 3
2 2 2
2 2 3
2 3 2
2 3 3
3 3 3
END