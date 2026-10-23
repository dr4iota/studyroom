The constraints below show which values each asked item can take. Then I check the one combination that is ruled out.

**Constraints that matter**
- C1 reads y = 0, so C1 takes effect before both writes to y (A1 and B3).
- Thread C finishes before Q, and B2 spans Q. Thread A's only sync line just puts A3's end after R, which never restricts anything. The P line in thread C only constrains steps above it, so P is easy to place. None of these limits the ordering of the writes to x.
- The writes to x are B1 (2), C2 (2), C3 (3), C4 (2), D1 (3), D2 (1) and D4 (1). C2, C3, C4 go in that order, and so do D1, D2, D4. B1 is free.

**Q1, the value A2 reads from x**
- **0:** do C1 and A1 first, then let A2 take effect before any write to x.
- **1:** A2 reads right after D2 and before D4.
- **2:** A2 reads right after B1, C2 or C4.
- **3:** A2 reads right after D1 or C3.

**Q2, the value D3 reads from y**
- **1:** D3 runs after A1 or B3.
- **0:** D3 runs before both A1 and B3.

**Q3, the final value of x**
- The last write to x must be C4 (2), B1 (2) or D4 (1), so the final value is 1 or 2.

**The excluded combination**
- If D3 returns 0, then D3 comes before A1. D1 and D2 come before D3, and A2 comes after A1. So D1 has already written x when A2 reads, and A2 cannot return 0.
- All other combinations can be built. For example, A2 = 1, D3 = 0, final 2 comes from this order: C1, D1, D2, D3, A1, A2, then C2, C3, C4, B1, D4, and finally B1 again is not needed. More simply: C1, D1, D2, D3, A1, A2, D4, then C2, C3, C4, B1, with B2, B3, B4 and A3 placed after them. The last write is B1, so x ends at 2.

BEGIN
0 1 1
0 1 2
1 0 1
1 0 2
1 1 1
1 1 2
2 0 1
2 0 2
2 1 1
2 1 2
3 0 1
3 0 2
3 1 1
3 1 2
END