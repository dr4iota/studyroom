"""Plugin registry shared by the linearization and solver APIs.

Algorithms are classes. A class becomes available by name when its module is imported
and it is decorated with ``@register``::

    @register
    class MyCounter(LinCounter):
        name = "my-counter"
        ...

The CLI also accepts ``--algo package.module:ClassName`` (imported on demand, no
registration needed) and ``--plugin package.module`` (imported so that its ``@register``
decorators run). This is how out-of-tree algorithms are plugged in.
"""

from __future__ import annotations

import importlib
from typing import Any, ClassVar, TypeVar

from .capabilities import Capabilities

A = TypeVar("A", bound=type)


class Algorithm:
    """Common base of every pluggable algorithm.

    Class attributes to set in subclasses:

    ``name``          registry name (``--algo NAME``)
    ``description``   one line, shown by ``list``
    ``capabilities``  :class:`Capabilities` (what it supports beyond the base problem)
    ``options``       ``{option: help}`` accepted as ``--opt option=value``; values are
                      parsed as YAML scalars (``3``, ``true``, ``abc``)
    """

    name: ClassVar[str] = ""
    description: ClassVar[str] = ""
    capabilities: ClassVar[Capabilities] = Capabilities()
    options: ClassVar[dict[str, str]] = {}
    category: ClassVar[str] = ""  # set by each API base class

    def __init__(self, **options: Any) -> None:
        unknown = set(options) - set(self.options)
        if unknown:
            raise ValueError(f"{self.name}: unknown option(s) {sorted(unknown)}; known: {sorted(self.options)}")
        self.opts = options


_REGISTRY: dict[str, dict[str, type[Algorithm]]] = {}


def register(cls: A) -> A:
    if not cls.name or not cls.category:
        raise TypeError(f"{cls.__name__} needs 'name' and a category (subclass an API base)")
    _REGISTRY.setdefault(cls.category, {})[cls.name] = cls
    return cls


def available(category: str) -> dict[str, type[Algorithm]]:
    return dict(sorted(_REGISTRY.get(category, {}).items()))


def resolve(category: str, spec: str, base: type[Algorithm]) -> type[Algorithm]:
    """Look up ``spec`` (a registered name or ``module:Class``) and check its API."""
    if ":" in spec:
        mod, _, attr = spec.partition(":")
        cls = getattr(importlib.import_module(mod), attr)
    else:
        try:
            cls = _REGISTRY.get(category, {})[spec]
        except KeyError:
            raise KeyError(f"no {category} algorithm {spec!r}; available: {', '.join(available(category))}") from None
    if not (isinstance(cls, type) and issubclass(cls, base)):
        raise TypeError(f"{spec} is not a {base.__name__}")
    return cls


def load_plugins(modules: list[str]) -> None:
    for m in modules:
        importlib.import_module(m)
