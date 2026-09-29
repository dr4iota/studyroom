import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
EXAMPLES = os.path.join(ROOT, "examples")

import harness.lin  # noqa: E402,F401  (register algorithms)
import harness.solve  # noqa: E402,F401
from harness.gen import generate  # noqa: E402


def example(name: str) -> str:
    return os.path.join(EXAMPLES, name)


def small_setups(n: int, **hp):
    """``n`` small generated setups (seeds 0..n-1) with the given hyperparameters."""
    base = {"threads": 2, "blocks": 2, "actions_per_thread": 2, "max_in_flight": 2}
    base.update(hp)
    for seed in range(n):
        yield generate({**base, "seed": seed})
