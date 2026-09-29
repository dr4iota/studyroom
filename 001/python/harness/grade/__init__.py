"""GRADE: the harness's grader for attempts (model-written algorithms).

    python -m harness grade --plugin attempts.<dir> [--algo NAME ...] [--budget small|full]

For every algorithm the plugin registers (or those named with ``--algo``):

1. static import policy (``policy.py``): attempts may use only the data model and APIs;
2. correctness on every case its capabilities cover (``instances.py``): generated
   instances plus a fixed adversarial suite, each checked against the harness oracles
   (``checks.py``), under a per-instance time limit;
3. throughput of enumerators on shared larger instances (informational).

The result is a ``report`` document (formats.md §8), subject ``grade``, ``ok`` iff there
are no errors. The grader caps its own address space (``--mem-mb``, default 2000).
Attempts never run their own tests; this grader is the only judge.
"""
