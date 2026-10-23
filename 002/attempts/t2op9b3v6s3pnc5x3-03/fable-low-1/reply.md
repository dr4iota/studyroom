**Analysis**

- **A1** reads z before A3 writes 5; only B3 (3) can precede it besides the initial 0 → A1 ∈ {0, 3}.
- **A5** reads x; candidates are B1 (5) or A4 (value of A2 ∈ {0,3}). B7 is after Q > A9 > A5, so excluded. If A1 = 3 then A2 = 3, so A5 ∈ {3,5}; if A1 = 0, A5 ∈ {0,3,5}.
- **Final z** = B9's value (B9 is after P and after Q, thus after A3, B3, A9). B9 writes B2's value. B2 reads 0 (before A3) or 5 (after A3); it cannot read A9's value since A9 > A6 > B3 > B2 would be needed for a 3, which is circular. So final z ∈ {0,5}.
- Couplings: A1 = 3 ⇒ B3 < A3 ⇒ B2 < A3 ⇒ final z = 0. Final z = 5 ⇒ B3 after A3 ⇒ A2 = 0 ⇒ A5 ∈ {0,5}.

BEGIN
0 0 0
0 3 0
0 5 0
0 0 5
0 5 5
3 3 0
3 5 0
END