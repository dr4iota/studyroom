Final z is always the value B2 read, and A5 is always either A2's value or 5, so there are seven combinations in all.

**Constraints from the sync points**
- B5 starts after R, and all of A1–A5 end before R.
- B6 starts after Q, and all of thread A ends before Q.
- B7, B8 and B9 come after B6 in B's program order, so they run after every operation of thread A.

**Q3 (final z).** B9 writes B2's value and is the last write to z, so the final z equals B2's value. B2 runs before B3, so it cannot see 3. It reads either 0 (before A3) or 5 (after A3). If B2 ran after A9, A9 would have to write something B2 could see. But A6 comes after A3, so A6 can only return 3 if B3 ran first, and B2 runs before B3. So A9 would write 5, which is already in the allowed set. The final z is therefore 0 or 5.

**Q2 (A5).** A4 writes A2's value to x before A5 reads. B1 may write 5 to x before or after A4. B7 writes x only after all of A, so it cannot affect A5. So A5 is either A2's value or 5. A2 reads z before A3, so it returns 0, or 3 if B3 has already run.

**Case final z = 0.** B2 read 0, so B2 ran before A3.
- A1 = 0: A2 can be 0 or 3, so A5 can be 0, 3 or 5.
- A1 = 3: B3 ran before A1, so A2 = 3 and A5 can be 3 or 5.

**Case final z = 5.** B2 read 5, so A3 ran before B2 and B3 ran after A3. A1 and A2 therefore read 0. A5 can be 0 or 5.

BEGIN
0 0 0
0 3 0
0 5 0
3 3 0
3 5 0
0 0 5
0 5 5
END