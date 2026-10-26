**Reasoning**

- A5 happens after A4 (which writes 3), so A5 returns 3 unless B4 or B5 (which write B2's value) take effect between A4 and A5. So A5 ∈ {3} ∪ {value of B2}.
- B3 reads before B4/B5, so it sees only A's writes: the sequence of x values from A is 0 → 2 → 3 → 1 → 3, so B3 ∈ {0,1,2,3}.
- B2 reads before B3, so B2's value must come from a state no later than the one B3 saw:
  - B3 = 0 ⇒ B2 = 0
  - B3 = 2 ⇒ B2 ∈ {0,2}
  - B3 = 1 ⇒ B2 ∈ {0,2,3,1}
  - B3 = 3 ⇒ B2 ∈ {0,2,3,1} (the 3 may be seen after A4, so B2 could have seen 1)
- Each such B2 value can be written by B4 after A4 and before A5, making A5 return it; or B4/B5 can finish before A4, leaving A5 = 3.

BEGIN
0 0
3 0
0 1
1 1
2 1
3 1
0 2
2 2
3 2
0 3
1 3
2 3
3 3
END