Every operation takes effect at one instant, so the possible outcomes are the interleavings of the three threads' operations. Write a for the value A3 reads and b for the value B2 reads. Write c for the value C1 reads.

**Possible values of a and b.** B1 writes 2 to y before B2, so b is 1 or 2 (it is 1 only if C4 falls between B1 and B2). The value a can be 0, 1 or 2.

**What can be last to write x.** A4 is always followed by A5, and B4 is always followed by B5, so neither can be last. The last write is therefore A5 (value 3), B5 (value b) or C2 (value c).

**Case 1: A5 is last, so x = 3.**
- All three values of a (0, 1, 2) can occur, and each can occur with y = 1 or y = 2.
- y ends as 1 if C4 comes after B3. It ends as 2 if B3 writes 2 and C4 is not later.
- This gives 6 outcomes.

**Case 2: B5 is last with b = 1, so x = 1.**
- C4 occurs between B1 and B2, so B3 also writes 1 and y = 1.
- a can be 0, 1 or 2.
- This gives 3 outcomes.

**Case 3: B5 is last with b = 2, so x = 2.**
- C4 is before B1 or after B2.
- y = 1 if C4 comes after B3, and y = 2 otherwise.
- a can be 0, 1 or 2 with either y.
- This gives 6 outcomes.

**Case 4: C2 is last.**
- A and B are finished before C2, so C3 and C4 come after them and y = 1.
- C4 is after A3, so a cannot be 1.
- C1 can read 0 (read first), 1 (after A1), 2 (after B4 or B5) or 3.
- The new outcomes are x = 0 with a = 0 or a = 2, giving 2 outcomes. The other x values from this case duplicate the earlier cases.

BEGIN
0 3 1
0 3 2
1 3 1
1 3 2
2 3 1
2 3 2
0 1 1
1 1 1
2 1 1
0 2 1
0 2 2
1 2 1
1 2 2
2 2 1
2 2 2
0 0 1
2 0 1
END