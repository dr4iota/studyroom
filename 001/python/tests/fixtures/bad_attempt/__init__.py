"""A deliberately wrong attempt: every algorithm has a planted bug the grader must catch."""

from harness.capabilities import Capabilities
from harness.lin.api import CountResult, LinCounter, LinEnumerator
from harness.lin.backtrack import linear_extensions  # IMPORT-POLICY: reference code
from harness.registry import register
from harness.solve.api import Outcomes, Solver, SolverCapabilities


@register
class DropsLast(LinEnumerator):
    name = "bad-drops-last"
    capabilities = Capabilities(sync=True)

    def enumerate(self, setup):
        orders = list(linear_extensions(setup))
        yield from orders[:-1]  # MISSING


@register
class IgnoresObservations(LinEnumerator):
    name = "bad-ignores-obs"
    capabilities = Capabilities(sync=True, observed_reads=True)

    def enumerate(self, setup):
        yield from linear_extensions(setup)  # EXTRA on instances with infeasible L


@register
class Crashes(LinEnumerator):
    name = "bad-crashes"
    capabilities = Capabilities()

    def enumerate(self, setup):
        raise RuntimeError("planted crash")


@register
class OffByOne(LinCounter):
    name = "bad-off-by-one"
    capabilities = Capabilities()

    def count(self, setup):
        return CountResult(sum(1 for _ in linear_extensions(setup)) + 1, None, "bad")  # COUNT


@register
class InitOnly(Solver):
    name = "bad-init-only"
    capabilities = SolverCapabilities(modes=frozenset({"all"}))

    def solve(self, setup, linearization=None):
        return Outcomes("all", True, {a.id: {setup.init[a.block]} for a in setup.returning()},
                        {b: {setup.init[b]} for b in range(setup.blocks)})  # UNDER / OVER
