Only C4 writes to y, and it writes the value C1 read from z. So A2 can only return 0 (the initial value, or a write of 0) or a value C1 read from z.

- **0:** A2 runs before any write to y takes effect. This is possible.
- **2:** B1 writes 2 to z, then C1 reads 2, then C4 writes 2 to y, and then A2 reads 2. Since A2 precedes A4 in thread A, nothing needs to overwrite z or y in between. This is possible.
- **4:** A2 would have to come after C4 writes 4 to y. That requires C1 to read 4, which requires A4 (the only write of 4 to z that can precede C1, since C5 comes after C4) to happen before C1. But A2 comes before A4 in thread A, so A2 would have to come after A4, which is a contradiction. This is impossible.

BEGIN
0
2
END