# Case study: `t2op9b3v6s4pnc5x5q4-04`

Two threads, nine operations each, four sync points. A person can solve it on paper in a
few minutes, yet at effort `low` 19 of 36 model runs got it wrong, and only Haiku was
perfect, at `high`.

## The problem

All blocks start at 0. Notation: `z:=6` writes 6 to z, `z?` reads z, `z:=A4` writes the
value A4 read; `(→S)` means every step to its left happens before instant S, `(S→)` that
every step to its right happens after S.

```
A:  A1 z:=6 (→S) A2 x:=1 (P→) A3 x? A4 z? A5 y? A6 z:=A4 A7 z? A8 y:=A7 (Q→) A9 z:=A4 (→R)
B:  B1 z:=1 (→P) B2 y? (→Q) B3 x? B4 y? (S→) B5 x:=3 B6 x:=B3 B7 x:=4 (R→) B8 z:=B2 B9 z?

Asked: (B9, final x, final y, final z)
```

The same problem in YAML (the model saw the plain-text form of
[`problem.txt`](../problems/t2op9b3v6s4pnc5x5q4-04/problem.txt) under prompt v1):

```yaml
blocks: [x, y, z]            # all start at 0
sync: [P, Q, R, S]
threads:
  A:
    - {op: A1, write: z, value: 6}
    - {sync: before S}
    - {op: A2, write: x, value: 1}
    - {sync: after P}
    - {op: A3, read: x}
    - {op: A4, read: z}
    - {op: A5, read: y}
    - {op: A6, write: z, copy: A4}
    - {op: A7, read: z}
    - {op: A8, write: y, copy: A7}
    - {sync: after Q}
    - {op: A9, write: z, copy: A4}
    - {sync: before R}
  B:
    - {op: B1, write: z, value: 1}
    - {sync: before P}
    - {op: B2, read: y}
    - {sync: before Q}
    - {op: B3, read: x}
    - {op: B4, read: y}
    - {sync: after S}
    - {op: B5, write: x, value: 3}
    - {op: B6, write: x, copy: B3}
    - {op: B7, write: x, value: 4}
    - {sync: after R}
    - {op: B8, write: z, copy: B2}
    - {op: B9, read: z}
asked: [B9, final x, final y, final z]
answer: [[0,1,1,0], [0,1,6,0], [0,4,1,0], [0,4,6,0], [1,4,1,1], [6,4,6,6]]
```

## Solving it by hand

**1. What the sync points order.** Read each line against the step it touches:
- P: B1 < A3. Q: B2 < A9. S: A1 < B5.
- R: all of A (A1–A9) < B8, B9.

**2. z ends with B2's value.** By R, B8 comes after every write in A, and it is B's last
write to z. So B8 writes z last, and B9 reads it. Call B2's value *b*: B9 = final z = *b*.

**3. A4 reads 1 or 6.** Before A4, z is written by A1 (6) and B1 (1, before A3 by P).
Nothing orders A1 and B1, so A4 reads *v* ∈ {1, 6}.

**4. y ends as v.** A6 writes *v* to z, and A7 reads it back: no other write to z can fall
between them (B1 is before A3; B8 is after all of A). A8, the only write to y, writes it.

**5. b is 0 or v.** B2 reads y: 0 before A8, *v* after A8. Q only puts B2 before A9, so
both are possible.

**6. x ends as 4 or 1.** B7 (4) is B's last write to x. A2 (1) is not tied to any sync
point (`(→S)` is above it, `(P→)` below it), so it can come after B7.

**7. The catch: x = 1 forces b = 0.** If A2 follows B7, then B2 < B7 < A2 < A8, so B2
reads y before A8 writes it.

So (B9, x, y, z) = (*b*, x, *v*, *b*) with *v* ∈ {1, 6}, *b* ∈ {0, *v*}, and *b* = 0 when
x = 1:

```
0 1 1 0 | 0 1 6 0 | 0 4 1 0 | 0 4 6 0 | 1 4 1 1 | 6 4 6 6
```

## How the models did

One shot, no tools, 9 trials per model and effort (Fable 5.1, Opus/Sonnet/Haiku 5.5):

| effort | fable51 | opus55 | sonnet55 | haiku55 |
|---|---|---|---|---|
| low | 0/9 | 6/9 | 5/9 | 6/9 |
| medium | 3/9 | 8/9 | 6/9 | 8/9 |
| high | 7/9 | 8/9 | 6/9 | 9/9 |

## Where they went wrong

All 36 wrong runs gave one of six answers. Each breaks one step above:

| runs | answer given | broken step | example from a reply |
|---|---|---|---|
| 14 | adds `1 1 1 1`, `6 1 6 6` | 7: treats x and *b* as independent | "Final x is 1 or 4. For each choice of x: …" (opus55-low-2) |
| 10 | drops `1 4 1 1`, `6 4 6 6` | 5: reads `(Q→)` as ordering A8 | "The only write to y is A8, and it happens after Q. B2 happens before Q, so B2 reads 0." (sonnet55-high-1) |
| 8 | drops `0 1 1 0`, `0 1 6 0` | 6: reads `(R→)` as ordering B7 | "B7 (write 4) is after R, so final x = 4." (fable51-medium-3) |
| 2 | keeps only *v* = 1 | 3: takes B1 as the last write | "B1 precedes A3, so A4 reads z = 1." (haiku55-low-4) |
| 2 | other | mixes of the above | |

**Takeaways**
- Two of the three main errors are misreadings, not missing logic: a sync line is taken
  to order the operation next to it on the wrong side. The rule in the prompt is clear,
  but models attach the line to the adjacent step.
- The most common error keeps every fact right but loses the one coupling between
  variables (step 7): models enumerate x and *b* separately.
- More effort helps where a re-check catches the slip (Haiku 6 → 9 of 9, Fable 0 → 7).
  Sonnet's misreading of Q survives `high` effort (3 of 9 runs).
