Both final-y values are possible, and z always ends at 3.

**Deductions from the known reads**

- A3 reads z as 0 after A2 wrote the value of A1 to z. The only write that can leave 0 in z is A2 itself, so A1 read 0. That makes A2, A4, A5 and A7 all write 0, and no other write to z can fall between A2 and A3.
- C5 reads y as 4, so B4 (the only write of 4 to y) happens before C5.
- A8 reads x as 4. The only write of 4 to x is C7, whose value comes from C5. So A4 < C7 < A8 and C7 < B7.
- The only writes to y are A5 (0), A7 (0) and B4 (4).

**Final y**

- **y = 0:** B4 < A7 is consistent. Order A1–A3 early, then A5, A6, with B4 falling before A5 or after A6, then A7, then C5, C7 and A8. All known reads hold.
- **y = 4:** A7 < B4 is consistent. A7 < B4 < C5 < C7 < A8, with B2 and B3 before B4 (reading 0). All known reads hold.

**Final z**

- B1 writes 2 but precedes B5, so it cannot be last.
- A2 cannot be last. B8 reads 3 after B5 (z = 3), so B8 would have to come before A2. But B7 comes after C7, which is after A4, which is after A3, which is after A2. That is a contradiction.
- C1 and C2 precede C3, so they cannot be last.
- The last write to z is therefore B5 or C3, both writing 3, so z = 3.

BEGIN
0 3
4 3
END