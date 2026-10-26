Possible triples, in the order A2 B1 C4:

- B1 is always 0 or 3. The only source of a 2 in x is B4 (copying a y value of 2), and B4 comes after B1 in thread B, so B1 can never read 2.
- A2 can be 0 (before any write to x), 3 (after C1), or 2 (after B4 writes 2).
- C4 reads x after C1 has written 3, so any 0 it sees must come from B4 writing 0 after C1. That needs B2 to have read y=0, so B2 precedes A1, and A2 comes after A1. C4 can also be 2 (B4 writes 2 after C1) or 3.
- The one excluded combination is A2=2 with C4=0. For C4=0, B4 must write 0, which needs B2 to read y=0. That forces B2 before A1, and B4 is then the only write to x of a value other than 3. So 2 is never written to x, and A2 cannot read it.
- Every other combination can be scheduled for both B1=0 and B1=3.

BEGIN
0 0 0
0 0 2
0 0 3
0 3 0
0 3 2
0 3 3
2 0 2
2 0 3
2 3 2
2 3 3
3 0 0
3 0 2
3 0 3
3 3 0
3 3 2
3 3 3
END