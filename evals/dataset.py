"""Loads the golden dataset and turns it into DeepEval test cases."""

import json
from pathlib import Path

from deepeval.dataset import EvaluationDataset, Golden
from deepeval.test_case import LLMTestCase

from app.support_bot import answer, knowledge_base

GOLDENS_PATH = Path(__file__).resolve().parent.parent / "data" / "goldens.json"


def load_goldens() -> list[Golden]:
    rows = json.loads(GOLDENS_PATH.read_text())
    return [Golden(input=r["input"], expected_output=r["expected_output"]) for r in rows]


def build_test_case(golden: Golden) -> LLMTestCase:
    """Run the app on one golden and package the result for the judge."""
    return LLMTestCase(
        input=golden.input,
        actual_output=answer(golden.input),
        expected_output=golden.expected_output,
        context=[knowledge_base()],
    )


def build_dataset() -> EvaluationDataset:
    return EvaluationDataset(goldens=load_goldens())
