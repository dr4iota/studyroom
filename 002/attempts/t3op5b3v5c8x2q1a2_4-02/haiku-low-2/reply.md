Only two values are possible for A2: **0** and **4**.

- **0:** A2 runs before any write to x takes effect. This is possible, since no thread has to act first.
- **4:** Run C1 (y := 4), then C4 (reads y = 4), then C5 (x := 4), then A2 (reads x = 4). A4 comes after A2 in thread A, so it cannot interfere.
- **1 and 2 are impossible:** A2 can only see writes to x that took effect before A2. A4 comes after A2, so the only possible source is C5, which writes the value C4 read from y. The only writes of 1 or 2 to y come from B4, which copies a value B3 read from x. So the first write of 1 or 2 to x would need an earlier write of 1 or 2 to x, which is circular. The only other source, A4, is ruled out because it runs after A2.

BEGIN
0
4
END