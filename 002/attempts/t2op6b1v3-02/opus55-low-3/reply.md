Each line below is one valid combination of (B1, B4, final x). B1 must come before B3, B4 sits between B3 and B5, and A's writes (A3=2, A4=3, A5=2) happen in order.

**What B1 can return (B1 happens before B3):**
- **0** if B1 happens before A3.
- **2** if B1 happens after A3 but before A4, or after A5.
- **3** if B1 happens after A4 but before A5.

**What B4 can return (between B3 and B5):**
- **1** if no write by A happens between B3 and B4.
- Otherwise B4 returns the last write by A between B3 and B4, which is 2 or 3.

**Final value:**
- **1** if B5 is the last write.
- **2** if A5 is the last write.

**Combinations:**
- **B1=0:** A3, A4 and A5 all come after B1.
  - B4=1, 2 or 3 are all possible.
  - B4=1: the final value can be 1 or 2.
  - B4=2 or 3: A5 can still come after B4, so the final value can be 1 or 2. For example, the order B1, B3, A3, B4, A4, B5, A5 gives B4=2 and final 2.
- **B1=2:**
  - B4=1: final 1 or 2.
  - B4=3: A4 falls between B3 and B4 while A5 can come later, so final 1 or 2.
  - B4=2: this needs A5 before B4, because A3 already came before B1. B5 then writes last, so the final value is 1.
- **B1=3:** A4 already happened before B1.
  - B4=3 is impossible. A4 came before B3, and no later write of 3 exists.
  - B4=1: final 1 or 2.
  - B4=2: A5 is between B3 and B4, so final 1.

BEGIN
0 1 1
0 1 2
0 2 1
0 2 2
0 3 1
0 3 2
2 1 1
2 1 2
2 2 1
2 3 1
2 3 2
3 1 1
3 1 2
3 2 1
END