Only five writes can change the blocks: D1, C3, C4 for y, and D3, A3 for x.

**Values y can hold.** C2 runs before C3, so it can only read 0 or 3 (D1's value). C4 therefore writes 0 or 3. C3 is always followed by C4, so C3 can never be the last write to y. The final y is therefore 0 or 3.
- y = 0: C2 reads 0, then D1 and C3 happen, and C4 writes 0 last.
- y = 3: D1 is the last write, or C4 writes 3 after C2 read 3.

**Values x can hold.** D3 writes whatever D2 read, which can be 3 (D1), 2 (C3) or 0. A3 writes whatever A2 read, which is 0 or D3's value. So x only ever holds 0 or one single value v ∈ {2, 3} from D3, and A3 can only rewrite x to 0 or v. This means x never holds both 2 and 3.

**A1 and B3.**
- A1 = 0: B3 can be 0, 2 or 3, since D3's value can be anything and B3 may read at any time.
- A1 = 2: D3 wrote 2, so no 3 can appear. B3 can be 0 (read early) or 2.
- A1 = 3: B3 can be 0 or 3, for the same reason.

**Pairing with y.** Each pairing works with either final y.
- A1 = 2, y = 0: C2 reads 0, then D1, C3, D2 (reads 2), D3, A1, and finally C4 writes 0.
- A1 = 2, y = 3: D1, C2 (reads 3), C3, D2 (reads 2), D3, A1, then C4 writes 3.
- A1 = 3, y = 0: C2 reads 0, then D1, D2 (reads 3), D3, A1, C3, and finally C4 writes 0.
- A1 = 3, y = 3: D1, D2 (reads 3), D3, A1 give x = 3, and y ends at 3 after C3 and C4.
- A1 = 0: the same schedules work with A1 reading before D3.

BEGIN
0 0 0
0 0 3
0 2 0
0 2 3
0 3 0
0 3 3
2 0 0
2 0 3
2 2 0
2 2 3
3 0 0
3 0 3
3 3 0
3 3 3
END