Final y is always 3, and final z can be 2 or 3.

**Final y.** The writes to y are A4 (3), A5 (2), B1 (3) and B7 (3, since B4 returned 3).
- C2 returned 2, and the only write of 2 to x that can come before C2 is A8. So A7 must have read 2 from y, and A8 then wrote 2 to x before C2. (C5 also writes 2 to x, but it comes after C2.)
- C7 returned 3, so the last write to x before C7 is 3. C5 and A8 both wrote 2 and come earlier, so B6 (which writes 3) must come after A8 and C5, and before C7.
- B7 comes after B6, which comes after A8, which comes after A5.
- The only write of 2 to y is A5, so after A5 every write to y is a 3, and B7 is one of them. Final y is therefore 3.

**Final z.** The writes to z are B3 (2), B5 (3), B8 (3), C1 (3), C3 (2), C4 (4) and C8 (2).
- C6 reads 3 after C3 and C4, so B5 must come after C4 and before C6.
- C8 comes after C7, which comes after C4, so C4 cannot be the last write to z. Final z is therefore not 4.
- B8 only has to come after B6, which comes before C7. B8 can fall before C8, leaving 2 as the final value. B8 can also fall after C8, leaving 3. Both orders are consistent with all the known read results.

BEGIN
3 2
3 3
END