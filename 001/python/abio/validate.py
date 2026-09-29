"""``abio validate``: minimal validators (VAL-LIN, VAL-SOLVE by differential oracle).

    abio validate lin   SETUP LIN.yaml                  every document of the stream
    abio validate solve SETUP OUTCOMES.yaml [--oracle brute] [--lin LIN.yaml --index I]

Both write a ``report`` document and exit 0 iff ok. Error codes:

validate-lin    UNKNOWN-STEP, DUPLICATE, MISSING, BAD-ORDER, WRONG-SETUP
validate-solve  CONSISTENT (disagreement on consistency), OVER (value the oracle does
                not have), UNDER (oracle value missing)
"""

from __future__ import annotations

import argparse

from . import cli_common as C
from . import terms as T
from .formats import FormatError, Output, load_document, load_documents, parse_linearization, parse_outcomes, report_doc
from .solve.api import Solver


def add_parser(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("validate", help="validators")
    vsub = p.add_subparsers(dest="val_cmd", required=True)
    lin = vsub.add_parser("lin", help="VAL-LIN: check linearization documents")
    lin.add_argument("setup")
    lin.add_argument("lin")
    lin.add_argument("-o", "--output", default="-")
    sol = vsub.add_parser("solve", help="VAL-SOLVE: compare outcomes against an oracle solver")
    sol.add_argument("setup")
    sol.add_argument("outcomes")
    sol.add_argument("--oracle", default="brute")
    sol.add_argument("--lin", help="for mode fixed: the linearization stream used")
    sol.add_argument("--index", type=int, default=0)
    sol.add_argument("-o", "--output", default="-")
    p.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> int:
    setup = C.load(args.setup)
    errors: list[dict] = []
    stats: dict = {}
    if args.val_cmd == "lin":
        docs = load_documents(args.lin)
        for i, d in enumerate(docs):
            if d.get("setup_id") != setup.id:
                errors.append({"code": "WRONG-SETUP", "where": {"index": i}, "message": f"setup_id {d.get('setup_id')!r}"})
                continue
            for code, step, msg in setup.poset.check(d.get("order") or []):
                errors.append({"code": code, "where": {"index": i, "step": step}, "message": msg})
        stats["linearizations_checked"] = len(docs)
        subject = "validate-lin"
    else:
        oracle = C.instantiate("solver", args.oracle, Solver, [])
        order = None
        if args.lin:
            try:
                order = parse_linearization(setup, load_documents(args.lin)[args.index])
            except (IndexError, FormatError) as ex:
                C.die(str(ex))
        ref = oracle.solve(C.admit(setup, oracle, False), order)
        ok, res, fin = parse_outcomes(setup, load_document(args.outcomes))
        if ok != ref.consistent:
            errors.append({"code": "CONSISTENT", "where": {}, "message": f"solver says {ok}, oracle {ref.consistent}"})
        cells = [({"id": k}, res.get(k, set()), ref.results.get(k, set())) for k in sorted(set(res) | set(ref.results))]
        cells += [({"block": b}, fin.get(b, set()), ref.final.get(b, set())) for b in range(setup.blocks)]
        for where, got, want in cells:
            for v in T.sorted_terms(got - want):
                errors.append({"code": "OVER", "where": where, "value": T.to_value(v), "message": "solver lists a value the oracle does not"})
            for v in T.sorted_terms(want - got):
                errors.append({"code": "UNDER", "where": where, "value": T.to_value(v), "message": "oracle value missing from solver"})
        stats["values_possible"] = sum(len(w) for _, _, w in cells)
        subject = "validate-solve"
    with Output(args.output) as out:
        out.write(report_doc(setup.id, subject, errors, stats))
    return 0 if not errors else 1
