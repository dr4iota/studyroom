**How the three values can vary**

- **B1** happens before B3, so it can only see A's writes or the initial value. Thread A writes 2, then 3, then 2. So B1 can return 0 (before A3), 2 (after A3 or after A5) or 3 (after A4 and before A5).
- **B4** comes right after B3 writes 1. It returns 1 unless one of A's writes takes effect between B3 and B4. If one does, B4 returns the last such write, which is 2 or 3.
- **The final value** is whichever takes effect last: A5 (which writes 2) or B5 (which writes 1).

**Case B1 = 0 (B1 takes effect before A3)**

All of A's writes are still free to take effect later, so every combination works:
- B4 = 1: no A write falls between B3 and B4. A5 can land before or after B5, so the final value is 1 or 2.
- B4 = 2: either A3 is the only A write between B3 and B4, or A5 is the last one there. In the first case the final value is 1 or 2.
- B4 = 3: A4 falls between B3 and B4 and A5 comes later. A5 can be before or after B5, so the final value is 1 or 2.

**Case B1 = 2**

- **If B1 sees A3 (after A3, before A4):**
  - B4 = 1 when A4 and A5 both come after B4. The final value is 1 or 2.
  - B4 = 3 when A4 is between B3 and B4 and A5 comes after B4. The final value is 1 or 2.
  - B4 = 2 is only possible if A5 lies between B3 and B4, because A3 is already before B1. B5 then comes after A5, so the final value is 1.
- **If B1 sees A5 (after A5):** all of A's writes are done. B4 returns 1 and the final value is 1.

**Case B1 = 3 (after A4, before A5)**

- B4 = 3 is impossible, because A4 has already taken effect before B3.
- B4 = 1: A5 comes after B4, so the final value is 1 or 2.
- B4 = 2: A5 lies between B3 and B4, so B5 comes after it and the final value is 1.

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