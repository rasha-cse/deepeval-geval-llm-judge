"""DeepEval + pytest: one test per golden, each graded by three G-Eval metrics.

Run with:   deepeval test run tests/test_support_bot.py
(or plain `pytest tests/` — `deepeval test run` adds a nicer summary table).
"""

import pytest
from deepeval import assert_test

from evals.dataset import build_test_case, load_goldens
from evals.metrics import all_metrics

GOLDENS = load_goldens()


@pytest.mark.parametrize("golden", GOLDENS, ids=[g.input[:40] for g in GOLDENS])
def test_support_bot(golden):
    test_case = build_test_case(golden)
    assert_test(test_case, all_metrics())
