Only writes to z can change its final value. Thread B writes 4, 2, then 5 in that order, and thread C writes 1 once. The last write to take effect is either B3 (value 5) or C2 (value 1). B2 and B1 can't be last because B3 follows them in thread B.

Both outcomes are reachable. The problem has no sync points or known read results, so the threads can interleave freely. Scheduling all of B before C2 gives 1, and scheduling C2 before B3 gives 5.

BEGIN
1
5
END