Only B4 writes to y, and it writes the value B3 read from z. B3 comes after B2 (which writes 4), so B3 returns 4, or 2 if C1 takes effect between B2 and B3. Therefore y is 0 until B4 and then v, where v is 4 or 2. A3 and C3 each read either 0 or v.

The final x is the last write among B1, C2, A4 and C4, subject to B1<B2<B3<B4, C1<C2<C3<C4 and A1<…<A5.

**A3=0, C3=0.** A2 must be 0, so A4 writes 0. C4 writes 0. B4 comes after both reads, and B1 can come after everything else. Final x is 0 or 3. C2 can't be last because C4 follows it.

**A3=0, C3=v.** B4 comes before C3, so B1 comes before C4. A4 writes 0 and C4 writes v. Final x is v (C4 last) or 0 (A4 last). This holds for v=4 and v=2.

**A3=v, C3=0.** C3 comes before B4, which comes before A3. B1 and C2 are before B4, so neither can be last. The last write is C4 (value 0) or A4 (value 0 if A2 read 0, or v if A2 read v). Final x is 0 or v.

**A3=v, C3=v.** B4 comes before both reads. C4 writes v, and A4 writes 0 or v. Final x is 0 or v.

BEGIN
0 0 0
0 0 3
0 4 4
0 4 0
0 2 2
0 2 0
4 0 0
4 0 4
2 0 0
2 0 2
4 4 0
4 4 4
2 2 0
2 2 2
END