Every thread's operations are totally ordered with no sync points, so any interleaving that respects each thread's program order is allowed.

**C2 (y after C1 wrote 1).** C2 can read 1 (nothing intervenes) or 2 (B1 writes between C1 and C2). It can also read 0: A1 and A2 read 0 early, C1 writes 1, then A3 writes 0 back to y before C2 reads. So C2 ∈ {0, 1, 2}.

**C4 (x after C3 wrote C2's value).** The only writers of x are B2 (writes 1), C3 (writes C2's value) and C6 (writes 2, which comes after C4). That limits C4 as follows:
- C2=0: x is 0 after C3. B2 can then write 1 before C4. C4 cannot be 2, since nothing writes 2 to x before C4. So C4 ∈ {0, 1}.
- C2=1: x is 1 after C3, and B2 only writes 1, so C4 = 1.
- C2=2: x is 2 after C3. B2 can then overwrite it with 1 before C4. So C4 ∈ {1, 2}.

**A4 (x).** A4 can read 0 (early, before any write to x), 1 (after B2) or 2 (after C6, which is after C4). A4 comes after A3, but this does not conflict with any of the C2/C4 cases above. For C2=0, A3 writes 0 after C1 and before C2, and A4 can still occur at any point in the x timeline. So all three A4 values combine with every valid (C2, C4) pair.

That gives 5 valid (C2, C4) pairs × 3 values of A4 = 15 combinations, listed in the order A4 C2 C4.

BEGIN
0 0 0
0 0 1
0 1 1
0 2 1
0 2 2
1 0 0
1 0 1
1 1 1
1 2 1
1 2 2
2 0 0
2 0 1
2 1 1
2 2 1
2 2 2
END