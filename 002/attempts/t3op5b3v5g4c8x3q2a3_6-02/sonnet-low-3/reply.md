Only a few of the possible (A3, B3) pairs can occur.

**Constraints on y.** Thread C has C1 (x=3) before C2. C2 reads y=1, so it falls after A1 and before A2. C5 reads y=2, so it falls after A2. Hence C1 < C2 < A2 < A3, and A3 always runs after C1 has written 3 to x.

**What A3 can read.** Only two operations write x: C1 (writes 3) and B4 (writes B3's value, which is 0, 1 or 2).
- A3 reads 3 if B4 has not taken effect after C1 and before A3.
- Otherwise A3 reads B4's value, which equals B3's value. This requires B4 to fall after C1 and before A3.

So A3 is either 3 or equal to B3. The pairs (A3=0, B3=1), (A3=1, B3=0) and so on are impossible.

**Each B3 value is reachable.**
- B3=0: B3 runs before A1.
- B3=1: B3 runs between A1 and A2.
- B3=2: B3 runs after A2.

**Each pair is consistent with B5 reading z=1.** Let B5 read z after A4 writes 1 and before A5 overwrites it, or after C4 writes 1.

- A3 = B3 (values 0, 1, 2): B4 is placed after C1 and before A3.
- A3 = 3: B4 is placed before C1 or after A3.

**Pairs:** (0,0), (1,1), (2,2), (3,0), (3,1), (3,2).

BEGIN
0 0
1 1
2 2
3 0
3 1
3 2
END