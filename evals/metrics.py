"""G-Eval metrics used by both the pytest suite and the standalone runner.

G-Eval asks an LLM judge to score an output against natural-language criteria.
You can give it either a one-line `criteria` (DeepEval writes the evaluation
steps for you) or explicit `evaluation_steps` (more stable scores, recommended).
"""

import os

from deepeval.metrics import GEval
from deepeval.models import AnthropicModel
from deepeval.test_case import SingleTurnParams
from dotenv import load_dotenv

load_dotenv()


def judge_model() -> AnthropicModel:
    """The LLM that grades outputs. Kept separate from the app's model on purpose."""
    return AnthropicModel(model=os.getenv("JUDGE_MODEL", "claude-opus-5-5"))


def correctness_metric() -> GEval:
    # Compares the answer with the reference answer, using explicit steps.
    return GEval(
        name="Correctness",
        evaluation_steps=[
            "Check whether the facts in 'actual output' contradict any facts in 'expected output'.",
            "Heavily penalize wrong numbers: prices, storage limits, time windows and file sizes.",
            "Penalize omission of the key fact needed to answer the question.",
            "Extra, harmless detail that is consistent with 'expected output' is acceptable.",
        ],
        evaluation_params=[
            SingleTurnParams.INPUT,
            SingleTurnParams.ACTUAL_OUTPUT,
            SingleTurnParams.EXPECTED_OUTPUT,
        ],
        model=judge_model(),
        threshold=0.7,
    )


def groundedness_metric() -> GEval:
    # Checks that the answer only uses the knowledge base (no hallucinations).
    return GEval(
        name="Groundedness",
        evaluation_steps=[
            "Identify every factual claim in 'actual output'.",
            "For each claim, check whether it is supported by 'context'.",
            "Any claim not supported by 'context' (an invented price, feature or policy) is a hallucination and should lower the score sharply.",
            "If the question cannot be answered from 'context', the output should say so rather than guess.",
        ],
        evaluation_params=[
            SingleTurnParams.INPUT,
            SingleTurnParams.ACTUAL_OUTPUT,
            SingleTurnParams.CONTEXT,
        ],
        model=judge_model(),
        threshold=0.7,
    )


def helpfulness_metric() -> GEval:
    # A criteria-only metric: DeepEval derives the evaluation steps itself.
    return GEval(
        name="Helpfulness & Tone",
        criteria=(
            "Determine whether 'actual output' directly answers the customer's "
            "question in 'input' in a friendly, professional and concise way "
            "(at most about four sentences), and gives a next step when it cannot help."
        ),
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
        model=judge_model(),
        threshold=0.6,
    )


def all_metrics() -> list[GEval]:
    return [correctness_metric(), groundedness_metric(), helpfulness_metric()]
