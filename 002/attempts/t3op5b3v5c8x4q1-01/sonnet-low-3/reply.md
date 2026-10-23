C4 can only return 2.

**Writers to y.** The writes to y are A2 (writes whatever A1 read), B3 (writes 4) and C2 (writes 2).

**What C3 = 2 tells us.** C3 reads z as 2, so A4 or A5 wrote 2 to z. That means A3 read y as 2, and since A2 precedes A3, A2 has already taken effect by then. A 2 is written to y only by C2 or by A2 copying a 2 that A1 read. In either case C2 takes effect before A3's read.

**What B4 = 2 tells us.** B4 reads y as 2 after B3 wrote 4. So some write of 2 to y takes effect after B3 and before B4.

**Why C4 cannot be 4.** C4 comes after C3, which comes after A3. It would return 4 only if a write of 4 to y took effect after the last write of 2 and before C4. The candidates are B3 and A2.
- A2 precedes A3, and A3 read 2. For A2 to be the last 4-writer, no 2 could be written after it, which contradicts A3 reading 2.
- If B3 takes effect after A3's read, a 2 must be written after B3 to satisfy B4. The only 2-writers are C2 and A2, and both must take effect before A3's read of 2. That leaves no 2 after B3, which contradicts B4 = 2.

So no 4 can be written after A3's read.

**Why C4 cannot be 0.** C2 has already written 2 to y before C4, so y is never 0 again.

**Why 2 is achievable.** Take the order C2, A1 (reads 2), A2 (writes 2), A3 (reads 2), A4 (writes 2 to z), B3 (writes 4), then another write of 2 to y. For example, C2 can come after B3 only if A3 can still read 2 earlier, which fails. So instead use: B1, B2, B3 (y=4), A1 reads 4, A2 writes 4, C2 writes 2, B4 reads 2, A3 reads 2, A4 writes 2 to z, C3 reads 2, C4 reads 2. This satisfies every known result.

BEGIN
2
END