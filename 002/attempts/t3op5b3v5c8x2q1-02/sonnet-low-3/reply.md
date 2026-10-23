A2 can return only 0 or 4.

**Which writes to x A2 can see.** The only writes to x are A4, B-thread none directly, and C5. A4 comes after A2 in thread A, so A2 can never see A4's value. A2 therefore returns 0 (initial) or the value C5 wrote.

**What C5 can write.** C5 writes whatever C4 read from y. C1 wrote 4 to y before C4, so C4 reads either 4 (from C1) or B4's value, if B4 took effect after C1 and before C4.

**What B4 can write.** B4 writes what B3 read from x. B3 cannot have read A4's write. If it had, then A2 (which precedes A4) would have to read x before B4, C4 and C5 all took effect, so C5's value could not have reached A2. That case adds nothing new anyway. B3 also cannot have read C5's write, because C5 depends on C4, which depends on B4, which depends on B3. That is circular. So B3 reads 0, and B4 writes 0.

**Resulting values.** C4 reads 4 or 0, so C5 writes 4 or 0. A2 can therefore return:
- 0, by reading x before any write to it.
- 4, by running C1, C4 (reading 4) and C5 before A2.

BEGIN
0
4
END