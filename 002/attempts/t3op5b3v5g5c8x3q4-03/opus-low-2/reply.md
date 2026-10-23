**Approach.** There are no sync points, so any interleaving that respects each thread's program order is allowed. The known read results restrict which interleavings count.

**1. What B5 = 2 tells us.**
- Three writes go to z: A1 writes 3, A4 writes 4, and B3 writes whatever B1 read.
- Only B3 can produce the value 2, so B3 is the last write to z before B5.
- So B1 must have returned 2.

**2. What B1 = 2 tells us about y.**
- The only writes to y are C1 (writes 2) and B4 (writes B1's value, which is 2).
- So C1 happens before B1.
- B2 comes after B1, and from that point y can only hold 2. So **B2 = 2**.
- Every write to y writes 2, so the **final value of y is 2**.

**3. What C2 = 3 tells us.**
- A1 must be the last write to z before C2.
- A1 can come before or after the B3–B5 stretch, since nothing forces an order between them. Either way is consistent.

**4. C4 (the read of x).**
- Two writes go to x: A3 writes 2 and C3 writes 5. C4 comes after C3.
- If no A3 falls between C3 and C4, then **C4 = 5**.
- If A3 falls between C3 and C4, then **C4 = 2**. This works because A3 only needs to follow A2, which follows C1.

**5. Final z.**
- A4 comes after A1, so the last write to z is either A4 or B3.
- If A4 is last, the final z is **4**. Example: A4 runs after B5.
- If B3 is last, the final z is **2**. This needs A4 before B3, and B5 still reads 2.

**6. All four combinations can occur together.** For example, this order gives C4 = 2 and final z = 2:

C1, A1, C2, C3, A2, A3, C4, A4, B1, B2, B3, B4, B5

- C2 reads 3, A2 reads 2, C4 reads 2, and B5 reads 2.
- Moving A3 after C4 gives C4 = 5.
- Moving A4 after B5 gives final z = 4.

BEGIN
2 2 2 2
2 2 2 4
2 5 2 2
2 5 2 4
END