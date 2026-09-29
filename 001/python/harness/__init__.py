"""harness: reference Python implementation of the trace-analysis problem class.

See ../premise.md (definitions), ../formats.md (documents) and README.md (layout, APIs).

Modules
    terms          terms and expressions (``a~b``)
    model          Setup / Thread / Step / Action; parsing and validation of setups
    poset          trace poset, linearizations as node-index tuples, VAL-LIN
    semantics      atomic-register interpreter, effect orders, full-schedule enumeration
    capabilities   Features (used by a setup) vs Capabilities (supported by an algorithm)
    registry       plugin registry for algorithms
    formats        document readers/writers
    gen            GEN: hyperparameters, expression helpers, generator
    lin            LIN-*: enumerator / counter / sampler APIs and algorithms
    solve          SOLVE-*: solver API and algorithms
"""

__version__ = "0.1.0"
