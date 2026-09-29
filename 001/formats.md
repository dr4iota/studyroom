# On-disk formats

Status: v2 draft, 2026-09-28. Vocabulary follows `premise.md` §0 (action, endpoint,
event, step, sync point). Programs are arrays of step objects with actions inline; there
is no separate action table.

## 0. Conventions

- **YAML is the primary syntax; JSON is always accepted.** Every document is restricted
  to the JSON data model: maps with string keys, lists, strings, integers, booleans,
  `null`. No anchors, merge keys, custom tags or multi-line scalars. A file may be
  `.yaml` or `.json` with identical structure.
- **Every document starts with `format` and `version`.** Readers reject an unknown
  format or unsupported version. Unknown extra keys are ignored by readers and preserved
  by tools that rewrite a document.
- **Terms are strings, except that a bare constant may be an integer.** `data: 17` and
  `data: "17"` are the same term. Writers emit an integer for a bare constant and a
  string for everything else; readers accept both everywhere a term or expression is
  expected.
- **Names.** Threads, actions and (optionally) events carry user-chosen ids matching
  `[A-Za-z_][A-Za-z0-9_]*` and containing **no dot**. Every name a tool derives contains
  a dot (`r1.done`, `t0.before.0`, `sync.0`, `init.1`), so user ids and derived names
  never collide and a reader tells them apart by looking for a dot.
- **Blocks and sync points are integers** `0..M-1` and `0..K-1`.
- **Per-id data is a list of objects with an `id` field**, never a map keyed by id (YAML
  would type the key as an integer, JSON as a string).
- **Collections stream.** Linearizations, schedules and trace steps are written one per
  YAML document (`---` separators) or one per line in JSON (JSON Lines). No envelope.
- **`meta`** is an optional free-form map on any document (`tool`, `seed`, `created`,
  `comment`, ...). Never semantically load-bearing.
- **Binding.** A setup has an `id` string; every derived document repeats it as
  `setup_id`, and validators refuse to combine documents whose `setup_id`s differ.

| `format` | produced by | consumed by | streamed |
|---|---|---|---|
| `hyperparams` | humans, experiment drivers | `gen` | no |
| `setup` | `gen`, humans | everything | no |
| `linearization` | `lin sample`, `lin enum` | `solve` (fixed-`L`), `validate` | yes |
| `schedule` | `gen --truth`, `solve` (witnesses), samplers, `replay` | `validate` | yes |
| `outcomes` | `solve` | `validate`, `compare` | no |
| `count` | `lin count` | `validate` | no |
| `trace` | `gen --stream`, adapters | `solve --online` | yes |
| `report` | `validate`, `compare` | humans, CI | no |

---

## 1. `setup` — a problem instance

```yaml
format: setup
version: 2
id: "ex-0001"
meta: {tool: gen, seed: 7}
blocks: 2                       # M
sync_points: 1                  # K; sync points are 0 .. K-1
init: [0, "*"]                  # per block: a term, or "*" = unknown (the term "init.<b>")
semantics:                      # optional; defaults shown
  register: atomic              # atomic | regular | safe
  rcw_result: old               # old (result = old content) | flag (ok / fail only)
  distinct_effects: true
threads:
  - id: t0
    steps:
      - {write: 0, id: w1, data: 1}
      - {read: 1, id: r1}
      - {done: w1}
      - {done: r1}                    # no data: result unobserved
      - {before: 0}
      - {write: 1, id: w2, data: r1~7}
      - {done: w2}
  - id: t1
    steps:
      - {after: 0}
      - {read: 0, id: r2}
      - {write: 1, id: w3, data: 9}
      - {done: r2, data: 1}           # observed result
      - {done: w3}
      - {rcw: 0, id: c1, expect: 1, data: 2}
      - {done: c1}                    # result unobserved
```

Each element of `steps` is one step, a map with exactly one of these *kind keys*:

| kind key | value | other fields | meaning |
|---|---|---|---|
| `read` | block | `id` (required) | start endpoint of a read |
| `write` | block | `id` (required), `data` (expr or `"*"`, required) | start endpoint of a write |
| `rcw` | block | `id` (required), `expect` (expr, required), `data` (expr or `"*"`, required) | start endpoint of a read-compare-write |
| `done` | action id | `data` (optional; reads and RCWs only) | end endpoint of that action; `data` is the observed result |
| `before` | sync point | `id` (optional) | event: this step precedes sync point `k` |
| `after` | sync point | `id` (optional) | event: this step follows sync point `k` |
| `at` | sync point | `id` (optional) | event: this step coincides with sync point `k` |

`N` is the length of `threads`. The number of actions is the number of
`read`/`write`/`rcw` steps.

Rules a reader enforces (violations make the setup malformed):

1. Action ids are unique across the whole setup. Each action has exactly one `done`,
   in the same thread, after its start step.
2. `done` of a write carries no `data`. `done` of a read or RCW may carry `data`:
   a term for a read; for an RCW a term (the old content), or `"ok"` / `"fail"` when
   `semantics.rcw_result` is `flag`. Absent `data` (or `"?"`) means unobserved.
3. Sync point values are in `0..K-1`. A thread has at most one event per
   (sync point, relation). A thread never has `after: k` before its own `before: k`
   or `at: k` (that is a cycle). Event ids, when given, are unique with the action ids.
4. The trace poset (`premise.md` §2.2) is acyclic.
5. Expressions satisfy §2.2 below. `init` has exactly `blocks` entries.

Knowledge is implicit: `p_w` is the fraction of `write`/`rcw` `data` fields that are
not `"*"`, `p_r` the fraction of read `done` steps that carry `data`.

### 1.1 Derived step names

Global lists (linearizations, schedules, traces, reports) refer to steps by name:

| step | name |
|---|---|
| start of action `x` | `x` |
| end of action `x` | `x.done` |
| event with an `id` | that id |
| event without an `id`, in thread `t`, relation `rel`, sync point `k` | `t.rel.k` (e.g. `t0.before.0`) |
| the virtual step of sync point `k` | `sync.k` |

`at` events never appear in a global list: their timestamp is that of `sync.k`.

---

## 2. Terms and expressions

### 2.1 Terms (values a block can hold)

```
term := item ( "~" item )*        left-associative: a~b~c means (a~b)~c
item := const | init | unk | "(" term ")"
const := [0-9]+                    17          a known constant (may be a bare integer in YAML/JSON)
init  := "init." [0-9]+            init.1      the unknown initial content of block 1
unk   := <write or rcw id>         w3          the unknown content of an action whose data is "*"
```

`a~b` is the ordered pair (a, b): a free constructor, so `a~b ≠ b~a`,
`a~(b~c) ≠ a~b~c`, and a pair never equals a constant, an `init.k` or an unknown.
Two terms denote the same content iff their trees are equal (`premise.md` §6
decision 6).

**Canonical form.** Writers print the minimal parenthesization: no parentheses at the
top level, none around a left operand, parentheses only around a right operand that is
itself a pair. Examples: `init.1~7`, `1~w4~init.0`, `r1~(r2~7)`. Readers
canonicalize on input, so comparing and sorting canonical strings is the same as
comparing trees.

### 2.2 Expressions (what a thread intends to write or compare)

Used in `data` and `expect`; same grammar with action ids as items:

```
expr := eitem ( "~" eitem )*
eitem := const | <read id> | <write or rcw id> | "(" expr ")"
```

- A read id stands for the value that read returned. The read's `done` step must
  precede the referencing step in the same thread.
- A write or RCW id stands for the content that action wrote (its evaluated
  expression, or its own id if its data is `"*"`). Its start step must precede the
  referencing step in the same thread. An RCW's content is what it *would* write;
  referencing it does not depend on whether it succeeded.
- `data: "*"` (the whole field) means unknown to the analyzer; the content is the term
  equal to the action's id.

Readers reject any other reference. A write executes by substituting the values of the
referenced actions, which yields a term; substitution keeps the tree shape, so
`data: r1~7` with `r1 = a~b` gives `(a~b)~7`, printed `a~b~7`.

**Why `~`.** Single ASCII character; safe unquoted in YAML block and flow context and
in JSON; safe as a shell argument and inside a file name; not part of identifiers; no
arithmetic reading and no commutative reading; and it has precedent as an ordered
"then" operator: string concatenation in Raku, ancestry in git (`HEAD~3`). A term is
never the bare `~` (YAML null) because a term always has at least one operand.
Ranked alternatives, in case this is revisited: `/` (path-like, but reads as division
and is not file-name safe), `;` and `|` (good "then" and "pipe" readings, but need
quoting in a shell), `^`, `-` (reads as subtraction), `_` (would have to be removed
from identifiers and makes `r1_7` look like one name). Excluded outright: `.` (dot
rule), `*` (unknown marker), `+` and `=` (commutative), `,` `:` `?` `[` `]` `{` `}`
(YAML/JSON structure), `"` `'` `\` `` ` `` (quoting), `#` `&` `@` `!` `%` `$` `<` `>`
(YAML indicators, shell operators or misleading readings).

---

## 3. `linearization` — one linear extension of the trace poset

```yaml
format: linearization
version: 2
setup_id: "ex-0001"
order: [w1, r1, w1.done, r1.done, t0.before.0, sync.0, t1.after.0,
        r2, w2, w3, r2.done, w2.done, w3.done, c1, c1.done]
```

`order` lists every start and end step, every `before`/`after` event by name, and
every `sync.k`, each exactly once; position (1-based) is the timestamp.

Validity (VAL-LIN): a permutation of exactly those names that respects each thread's
step order and the sync edges (`before` events precede their `sync.k`, `after` events
follow it; `at` events sit at it, so everything before an `at` in its thread precedes
`sync.k` and everything after it follows). Intervals follow:
`I(x) = [pos(x), pos(x.done)]`.

Optional annotations: `meta.index` (rank in an enumeration), `meta.weight`.

---

## 4. `schedule` — a full schedule (witness, ground truth, sample)

```yaml
format: schedule
version: 2
setup_id: "ex-0001"
order: [w1, r1, w1.done, r1.done, t0.before.0, sync.0, t1.after.0,
        r2, w2, w3, r2.done, w2.done, w3.done, c1, c1.done]
effects: [w1, r1, r2, w2, w3, c1]      # all action ids in effect order (π)
results:                               # derived by executing; one per read and per rcw
  - {id: r1, value: init.1}
  - {id: r2, value: 1}
  - {id: c1, value: 1}                 # rcw: the old content it found
final:                                 # one per block
  - {block: 0, value: 2}
  - {block: 1, value: 9}
consistent: true                       # every observed data in the setup matched
```

Validity (VAL-SCHED): `order` is a valid linearization; `effects` is a permutation of all
action ids admitting distinct instants `π(x) ∈ I(x)` in that order (checked greedily:
walk `effects` with a running instant `t := max(t + ε, pos(x))`, require
`t ≤ pos(x.done)`); `results`, `final` and `consistent` equal what the register
semantics produce. Validators recompute all three.

`results` and `final` are redundant with `order` + `effects`; they are required so a
schedule reads as a certificate without an interpreter at hand. `consistent: false`
is a legal document (samplers emit them) but certifies nothing.

---

## 5. `outcomes` — solver output

```yaml
format: outcomes
version: 2
setup_id: "ex-0001"
mode: all                       # all (over all linearizations) | fixed
linearization: null             # for mode fixed: path or meta.index of the L used
consistent: true                # false ⇒ CHECK failed; results/final omitted
results:                        # Poss(r) per read and per rcw; terms sorted, distinct
  - {id: r1, values: [init.1]}
  - {id: r2, values: [1]}
  - {id: c1, values: [1]}
final:                          # Poss(b) per block
  - {block: 0, values: [2]}
  - {block: 1, values: [9, init.1~7]}
witnesses: "ex-0001.witnesses.yaml"    # optional path to a schedule stream
```

Observed results list exactly their observed value. A witness stream holds one
`schedule` per (id-or-block, value) pair, each with `meta.certifies: {id: r1, value:
init.1}` or `{block: 1, value: 9}` and `consistent: true`.

Term order: canonical strings by length, then lexicographically
(`9` < `17` < `init.1~7`).

---

## 6. `count`

```yaml
format: count
version: 2
setup_id: "ex-0001"
linearizations: 126             # |Lin(P)| over the quotient poset
feasible: null                  # optional: count of feasible L given observations
method: dp-positions            # dp-positions | enumeration | estimate
error: null                     # for estimates: {relative: 0.05, confidence: 0.95}
```

---

## 7. `trace` — a step stream for the online solver

One document per step, in the order steps become known. A step document is exactly a
program step object plus `thread`, or a virtual step:

```yaml
---
format: trace
version: 2
setup_id: "ex-0001"
thread: t0
write: 0
id: w1
data: 1
---
format: trace
version: 2
setup_id: "ex-0001"
thread: t0
before: 0
---
format: trace
version: 2
setup_id: "ex-0001"
sync: 0                          # the virtual step sync.0
---
format: trace
version: 2
setup_id: "ex-0001"
thread: t1
done: r2
data: 1
```

A stream may start with a `setup` document whose threads have empty `steps`, giving
`blocks`, `sync_points`, `init` and `semantics` up front. Concatenating a stream
reproduces a setup plus a linearization. A write's content is revealed at its start
step and a read's result at its `done` step, matching the online reading of the
problem.

---

## 8. `report` — validator / comparator output

```yaml
format: report
version: 2
setup_id: "ex-0001"
subject: validate-solve         # validate-lin | validate-enum | validate-sched | validate-solve | compare
ok: false
errors:                         # empty when ok
  - {code: OVER,  where: {id: c1}, value: 2, message: "solver lists a value the oracle does not"}
  - {code: UNDER, where: {block: 1}, value: 9, message: "oracle value missing from solver"}
  - {code: BAD-ORDER, where: {step: t1.after.0}, message: "precedes sync.0"}
stats: {linearizations_checked: 3000, values_possible: 5, values_reached: 4}
```

Error codes form a closed list per subject, documented with the validator; codes may
be added, never renamed. Exit status is `0` iff `ok`.

---

## 9. `hyperparams` — generator input

```yaml
format: hyperparams
version: 2
seed: 7
threads: 2
blocks: 2
sync_points: 1
actions_per_thread: 3             # or total: {read: 4, write: 5, rcw: 1}
events_per_thread: 1
relations: [before, after, at]    # which event relations may be generated
max_in_flight: 2                  # 1 = synchronous I/O
kind_mix: {read: 0.5, write: 0.4, rcw: 0.1}
block_skew: {kind: zipf, s: 1.0}  # or {kind: uniform}
writers_per_block: null           # cap when set (hardness dial)
content:
  classes: {const: 0.5, copy: 0.3, combine: 0.2}   # premise §2.5 classes 1/2/3
  max_depth: 2
  value_pool: 8                   # distinct constants to draw from (small ⇒ repeats)
knowledge: {p_w: 0.9, p_r: 0.3, init_known: 0.5}
semantics: {register: atomic, rcw_result: old}
```

Every key has a default. `gen` records the resolved hyperparameters under
`meta.hyperparams` of the setup and, with `--truth`, writes the hidden run as a
`schedule` next to it.

---

## 10. Worked example

The setup of §1: thread `t0` writes `1` to block 0 while reading block 1, signals
sync point 0, then writes `r1~7` (that read's value, then 7) to block 1. Thread `t1`
waits on sync point 0, reads block 0 (observed `1`), writes `9` to block 1, then does
an RCW on block 0 expecting `1`.

- `r1` can only see the initial content: both writes to block 1 start after `sync.0`,
  which follows `r1.done`. `Poss(r1) = {init.1}`.
- `r2` starts after `sync.0`, hence after `w1.done`; `c1` starts after `r2.done`. The
  only write that can precede `r2` is `w1`: `Poss(r2) = {1}`, matching the observation.
- `c1` always finds `1` and succeeds: `Poss(c1) = {1}`; final block 0 is `2`.
- `w2` and `w3` are unordered: final block 1 is `9` or `init.1~7`.

The linearization of §3 and the schedule of §4 witness the `9` case; the outcomes
of §5 are the exact answer.

---

## 11. Versioning

- `version` is per document kind and bumps only on incompatible change; adding an
  optional key is not a bump. v1 (separate action table, token strings, `+` pairs) is
  withdrawn.
- The shared library owns all readers and writers; no component parses by hand.
- Round-trip property (tested): `read ∘ write = id` on the JSON data model for every
  kind, in YAML and JSON.
