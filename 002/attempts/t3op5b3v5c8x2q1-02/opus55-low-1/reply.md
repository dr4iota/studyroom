A2 can return **0** or **4**.

1. **Which writes could A2 see?** Only A4 and C5 write to x. A4 comes after A2 in thread A, so A2 can never see it. A2 therefore returns either 0 (no write to x yet) or the value C5 wrote.

2. **What can C5 write?** C5 writes the value C4 read from y.
   - C1 writes 4 to y before C4 runs, so C4 reads either 4 or the value B4 wrote, if B4 took effect after C1.
   - So C5 writes either 4 or B4's value.

3. **What can B4 write?** B4 writes the value B3 read from x. B3 has three options:
   - It reads 0.
   - It reads C5's value. This is impossible in the case that matters here. C4 reading B4's value needs B4 before C4, and B3 seeing C5 needs C5 before B3. That gives the cycle B3 < B4 < C4 < C5 < B3.
   - It reads A4's value, which is whatever A1 read from z.

4. **Can A2 see a value that came through A4?** That needs the order A4 < B3 < B4 < C4 < C5 < A2. But A2 comes before A4 in thread A, so this is a cycle and cannot happen.

5. **Conclusion.** If A2 sees C5's write, C5 wrote either 4 (C4 read C1's write) or 0 (C4 read B4's write, and B3 read 0). So A2 returns 0 or 4.

6. **Both values can occur.**
   - **0:** A2 runs before C5 takes effect.
   - **4:** C1, then C4 reads 4, then C5 writes 4 to x, then A2 reads x.

BEGIN
0
4
END