**Q1 (A9's read of x) is always 5.** Every write to x is B2 (1), B4 (1), A8 (5), or B9 (the value read by B8). B2 and B4 both precede A8. B8 comes after Q, which is after A8, so B8 reads 5, and B9 therefore writes 5. A9 comes after A8, so it reads 5 whether or not B9 has already happened.

**Q2 and Q3 (final y and z).** Let a4 be the value A4 reads from y. It is 6 if B5 falls between A2 and A4, and 4 otherwise.

- The final y is A6's write (a4) if B5 comes before A6, or 6 (from B5) if B5 comes after A6.
- The final z is A5's write (a4) if A5 comes after B3, or 6 (from B3) if B3 comes after A5. A3 and B1 can never be last.

Checking which pairs are jointly realizable:

- **(4, 4):** a4 = 4, B5 before A1, A5 after B3. Realizable.
- **(4, 6):** a4 = 4, order A1 A2 A3 A4 A5 B1 B2 B3 B4 B5 A6. Realizable.
- **(6, 4):** a4 = 6 needs B5 between A2 and A4, then A5 after B3. Realizable (order: A1 B1 B2 B3 A2 B4 B5 A3 A4 A5 A6).
- **(6, 6):** a4 = 6 with B5 between A2 and A4 and A5 after B3, so the final z is 6. Realizable (order: A1 B1 B2 B3 A2 B4 B5 A3 A4 A5 A6).

Final y = 4 with a4 = 6 is impossible, since A6 then writes 6.

BEGIN
5 4 4
5 4 6
5 6 4
5 6 6
END