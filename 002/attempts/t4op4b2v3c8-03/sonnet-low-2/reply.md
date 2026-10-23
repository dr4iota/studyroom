Values for x and y are limited by what each write can store.

**Values D2 can read.** D2 reads y after D1 has written 3. It can see 3, 2 (C3), or 0. The value 0 occurs when C2 read 0 and C4 then wrote 0, giving the order C2 → D1 → C3 → C4 → D2. So D2 ∈ {0, 2, 3}.

**Values x can hold.** The only writers of x are D3 and A3.
- D3 writes a single value v ∈ {2, 3}, or 0 if D2 read 0. The value 0 adds nothing new, because x already starts at 0.
- A3 only copies the value A2 read, which is 0 or v.
- So x only ever holds 0 and one nonzero value v, and every read of x returns 0 or v.
- A1 and B3 are not ordered against each other. A1 = v needs D3 to come first, and B3 can still read 0 before D3.
- So any pairing of A1 and B3 from {0, v} is possible. This includes (v, 0), (0, v), (v, v), and (0, 0). Different nonzero values for A1 and B3 are impossible.

**Final y.** The last write to y is either D1 (3) or C4. C4 comes after C3 and copies C2, which reads before C3, so C4 writes 0 or 3. A final y of 2 is therefore impossible.
- Final y = 0 needs C2 to read 0 and C4 to write last. D2 can still read 0, 2, or 3 beforehand, so v can be 2 or 3.
- Final y = 3 for v = 3: C4 writes 3 (C2 read 3), or D1 runs after C4 and D2 reads 3.
- Final y = 3 for v = 2: D1, C2 (reads 3), C3, D2 (reads 2), D3, then C4 writes 3.
- Final y = 3 with no nonzero v is also possible, since D3 can run late.

**Combinations (Q1 Q2 Q3).**
- With x staying 0: (0,0) with y = 0 or 3.
- With v = 2 or 3: pairs (0,v), (v,0), (v,v), each with y = 0 or 3.

BEGIN
0 0 0
0 0 3
0 2 0
0 2 3
2 0 0
2 0 3
2 2 0
2 2 3
0 3 0
0 3 3
3 0 0
3 0 3
3 3 0
3 3 3
END