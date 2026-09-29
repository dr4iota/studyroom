"""Terms and expressions (formats.md §2, premise.md §2.5).

A *term* is a value a block can hold. It is a tree built from

    Const(c)      a known natural-number constant           ``17``
    Init(b)       the unknown initial content of block b     ``init.1``
    Unk(x)        the unknown content of write/rcw ``x``     ``w3``   (its data is "*")
    Pair(l, r)    the ordered pair (l, r), printed ``l~r``   ``init.1~7``

An *expression* is what a thread intends to write (or compare, for RCW). It has the
same shape but its leaves are ``Const`` and ``Ref(x)``, where ``x`` is the id of an
earlier action of the same thread (a read's result, or a write's content).
Evaluating an expression (:func:`substitute`) replaces every ``Ref`` by a term.

``~`` is a free, non-commutative constructor: two terms are equal iff their trees are
equal. All node classes are frozen dataclasses, so ``==`` and ``hash`` are structural.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable, Iterable, Union


@dataclass(frozen=True, slots=True)
class Const:
    value: int

    def __str__(self) -> str:
        return format_term(self)


@dataclass(frozen=True, slots=True)
class Init:
    block: int

    def __str__(self) -> str:
        return format_term(self)


@dataclass(frozen=True, slots=True)
class Unk:
    """Unknown content of the write/rcw whose id is ``action`` (its data is ``"*"``)."""

    action: str

    def __str__(self) -> str:
        return format_term(self)


@dataclass(frozen=True, slots=True)
class Ref:
    """Expression leaf: the value of an earlier action ``action`` of the same thread."""

    action: str

    def __str__(self) -> str:
        return format_term(self)


@dataclass(frozen=True, slots=True)
class Pair:
    left: "Node"
    right: "Node"

    def __str__(self) -> str:
        return format_term(self)


Node = Union[Const, Init, Unk, Ref, Pair]
Term = Node  # a Node without Ref leaves
Expr = Node  # a Node whose leaves are Const or Ref


class TermSyntaxError(ValueError):
    pass


# --------------------------------------------------------------------------- printing


def format_term(t: Node, _right: bool = False) -> str:
    """Canonical form: parentheses only around a right operand that is a pair."""
    if isinstance(t, Pair):
        s = f"{format_term(t.left)}~{format_term(t.right, True)}"
        return f"({s})" if _right else s
    if isinstance(t, Const):
        return str(t.value)
    if isinstance(t, Init):
        return f"init.{t.block}"
    if isinstance(t, (Unk, Ref)):
        return t.action
    raise TypeError(f"not a term node: {t!r}")


def to_value(t: Node) -> int | str:
    """Document value of a term: a bare constant is an int, everything else a string."""
    return t.value if isinstance(t, Const) else format_term(t)


def sort_key(t: Node) -> tuple[int, str]:
    """Term order of formats.md §5: canonical string by length, then lexicographic."""
    s = format_term(t)
    return (len(s), s)


def sorted_terms(ts: Iterable[Node]) -> list[Node]:
    return sorted(set(ts), key=sort_key)


# --------------------------------------------------------------------------- parsing

_TOKEN = re.compile(r"\s*(?:(\d+)|(init\.\d+)|([A-Za-z_][A-Za-z0-9_]*)|(~)|(\()|(\)))")


def _tokens(s: str) -> list[tuple[str, str]]:
    out, i = [], 0
    s = s.rstrip()
    while i < len(s):
        m = _TOKEN.match(s, i)
        if not m or m.end() == i:
            raise TermSyntaxError(f"bad character at {i} in {s!r}")
        kinds = ("const", "init", "ident", "~", "(", ")")
        for k, g in zip(kinds, m.groups()):
            if g is not None:
                out.append((k, g))
        i = m.end()
    return out


def _parse(s: str, *, expression: bool) -> Node:
    toks = _tokens(s)
    if not toks:
        raise TermSyntaxError("empty term")
    i = 0

    def item() -> Node:
        nonlocal i
        if i >= len(toks):
            raise TermSyntaxError(f"unexpected end of {s!r}")
        k, g = toks[i]
        i += 1
        if k == "const":
            return Const(int(g))
        if k == "init":
            if expression:
                raise TermSyntaxError(f"'init.k' is not allowed in an expression: {s!r}")
            return Init(int(g[5:]))
        if k == "ident":
            return Ref(g) if expression else Unk(g)
        if k == "(":
            t = seq()
            if i >= len(toks) or toks[i][0] != ")":
                raise TermSyntaxError(f"missing ')' in {s!r}")
            i += 1
            return t
        raise TermSyntaxError(f"unexpected {g!r} in {s!r}")

    def seq() -> Node:
        nonlocal i
        t = item()
        while i < len(toks) and toks[i][0] == "~":
            i += 1
            t = Pair(t, item())
        return t

    t = seq()
    if i != len(toks):
        raise TermSyntaxError(f"trailing input in {s!r}")
    return t


def parse_term(v: int | str) -> Term:
    """Parse a term from a document value (int or string). Identifiers become ``Unk``."""
    if isinstance(v, bool):
        raise TermSyntaxError(f"not a term: {v!r}")
    if isinstance(v, int):
        if v < 0:
            raise TermSyntaxError(f"constants are natural numbers: {v}")
        return Const(v)
    if isinstance(v, str):
        return _parse(v, expression=False)
    raise TermSyntaxError(f"not a term: {v!r}")


def parse_expr(v: int | str) -> Expr:
    """Parse an expression from a document value. Identifiers become ``Ref``."""
    if isinstance(v, bool):
        raise TermSyntaxError(f"not an expression: {v!r}")
    if isinstance(v, int):
        if v < 0:
            raise TermSyntaxError(f"constants are natural numbers: {v}")
        return Const(v)
    if isinstance(v, str):
        return _parse(v, expression=True)
    raise TermSyntaxError(f"not an expression: {v!r}")


# --------------------------------------------------------------------------- building / evaluation


def seq(*items: Node | int | str) -> Node:
    """Left-associated chain ``a~b~c`` = ``Pair(Pair(a, b), c)``.

    Ints become ``Const``; strings become ``Ref`` (use explicit nodes for anything else).
    """
    if not items:
        raise ValueError("seq() needs at least one item")
    nodes = [Const(x) if isinstance(x, int) else Ref(x) if isinstance(x, str) else x for x in items]
    t = nodes[0]
    for n in nodes[1:]:
        t = Pair(t, n)
    return t


def refs(e: Node) -> set[str]:
    """Action ids referenced by an expression."""
    if isinstance(e, Pair):
        return refs(e.left) | refs(e.right)
    return {e.action} if isinstance(e, Ref) else set()


def depth(e: Node) -> int:
    """Number of ``~`` levels: a leaf has depth 0."""
    return 1 + max(depth(e.left), depth(e.right)) if isinstance(e, Pair) else 0


def substitute(e: Expr, lookup: Callable[[str], Term]) -> Term:
    """Evaluate an expression: replace every ``Ref(x)`` by ``lookup(x)``. Keeps tree shape."""
    if isinstance(e, Pair):
        return Pair(substitute(e.left, lookup), substitute(e.right, lookup))
    if isinstance(e, Ref):
        return lookup(e.action)
    return e
