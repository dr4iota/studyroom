**Reasoning:** A2 reads x before A4 (same thread), so A2 can only see 0 or the value written by C5. C5 writes what C4 read from y, and C4 reads either 4 (from C1), or a value written by B4 (B3's read of x). If B3's value came from A4, then A4 → B3 → B4 → C4 → C5 → A2 → A4 would be circular, impossible. So B3 contributes only 0, meaning C5 writes 0 or 4.

BEGIN
0
4
END