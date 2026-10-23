**Constraints from program order**

1. A5 is Thread A's only write, and it comes after A4. So A2 and A4 can only see the initial 0 or one of B's writes.
2. B's writes take effect in the order B2=1, B3=2, B4=3, B5=1. So x takes the values 0, 1, 2, 3, 1, in that order. A5 may add one more write of 1 somewhere.
3. A2 takes effect before A4. So A4 sees the same point in this sequence as A2, or a later one.

**Case B1 = 1**

B1 comes before B2, so this 1 must come from A5. Then A5 takes effect before B1, and so before B2. Because A2 and A4 come before A5, they also come before any of B's writes. So A2 = 0 and A4 = 0.

This gives one combination: 0 0 1.

**Case B1 = 0**

B1 takes effect before B2, and also before A5 if A5 comes early. Nothing else is restricted, so A2 and A4 can be any two points in the sequence 0, 1, 2, 3, 1, with A4 at the same point or later.

| A2 sees | Possible A4 values |
|---|---|
| 0 (before B2) | 0, 1, 2, 3 |
| 1 (after B2) | 1, 2, 3 |
| 2 (after B3) | 2, 3, 1 |
| 3 (after B4) | 3, 1 |
| 1 (after B5) | 1 |

**B1 cannot be anything else**

B1 takes effect before every one of B's writes. So it can only return 0, or 1 from A5.

BEGIN
0 0 1
0 0 0
0 1 0
0 2 0
0 3 0
1 1 0
1 2 0
1 3 0
2 1 0
2 2 0
2 3 0
3 1 0
3 3 0
END