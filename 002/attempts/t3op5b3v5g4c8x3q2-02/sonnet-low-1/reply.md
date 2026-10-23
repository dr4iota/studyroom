Every combination of A3 and B3 below is possible; the reasoning follows.

**Ordering constraints**
- Thread A writes y=1 (A1) and then y=2 (A2). C2 reads 1, so it falls between A1 and A2. C5 reads 2, so it falls after A2.
- C1 writes x=3 before C2. Since C2 comes before A2, and A3 comes after A2, C1 comes before A3. So A3 never reads 0.
- The writes to x are C1 (value 3) and B4 (the value B3 read). A3 therefore reads either 3 or the value B4 wrote, and B4 must fall after C1 and before A3 for A3 to see its value.
- B5 reads z=1. This is satisfiable because C4 writes 1 after C3 and B5 can read right after C4. It places no restriction on the other operations.

**Cases by B3**
- **B3 = 0:** B3 comes before A1, so B4 writes 0. The order B3, A1, C1, B4, C2, A2, A3 gives A3 = 0. Placing C1 after B4 gives A3 = 3. 
- **B3 = 1:** B3 falls between A1 and A2, so B4 writes 1. The order C1, A1, B3, B4, C2, A2, A3 gives A3 = 1. Placing C1 after B4 gives A3 = 3. 
- **B3 = 2:** B3 comes after A2, so B4 writes 2. The order A2, B3, B4, A3 (with C1 earlier) gives A3 = 2. Placing C1 after B4 gives A3 = 3. 

BEGIN
0 0
3 0
1 1
3 1
2 2
3 2
END