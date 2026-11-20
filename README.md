# DeepEval + G-Eval Sample Project

A small, complete example of **evaluating an LLM application with [DeepEval](https://github.com/confident-ai/deepeval)'s G-Eval metric**.

The app under test is a customer-support assistant for a fictional product, "Acme Cloud Storage". It answers questions with Claude, using a small knowledge base. DeepEval then uses a second LLM as a **judge** to score each answer against criteria written in plain English.

## What is G-Eval?

G-Eval ([Liu et al., 2023](https://arxiv.org/abs/2303.16634)) is an "LLM-as-a-judge" method:

1. You describe what "good" looks like, either as one-line `criteria` or as explicit `evaluation_steps`.
2. The judge LLM follows those steps to score the output from 0 to 1.
3. A test case passes when its score is at or above the metric's `threshold`.

This project defines three G-Eval metrics in [`evals/metrics.py`](evals/metrics.py):

| Metric | Compares | Style | Threshold |
|---|---|---|---|
| **Correctness** | answer vs. reference answer | explicit `evaluation_steps` | 0.7 |
| **Groundedness** | answer vs. knowledge base (`context`) | explicit `evaluation_steps` | 0.7 |
| **Helpfulness & Tone** | answer vs. question | `criteria` only (steps generated) | 0.6 |

## Project structure

```
deepeval-geval-sample/
├── app/
│   ├── support_bot.py        # LLM app under test (Claude via the Anthropic SDK)
│   └── knowledge_base.md     # Facts the bot is allowed to use
├── data/
│   └── goldens.json          # Questions + reference answers
├── evals/
│   ├── metrics.py            # G-Eval metric definitions + judge model
│   └── dataset.py            # Goldens -> LLMTestCase (runs the app)
├── tests/
│   └── test_support_bot.py   # pytest / `deepeval test run` suite
├── run_eval.py               # Standalone evaluate() run with a summary
├── .github/workflows/eval.yml  # Runs the evals on every pull request
├── requirements.txt
└── .env.example
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then put your ANTHROPIC_API_KEY in .env
```

## Run the evaluation

As a pytest suite (one test per golden, three metrics each):

```bash
deepeval test run tests/test_support_bot.py
```

Or as a standalone script with an average score per metric:

```bash
python run_eval.py
```

Try the bot on its own:

```bash
python -m app.support_bot "Can I get a refund after a month?"
```

## Choosing models

- `APP_MODEL` is the model the support bot uses.
- `JUDGE_MODEL` is the model DeepEval uses to grade answers.

Both default to `claude-opus-5-5`. A capable judge gives more reliable scores. To use OpenAI or another provider as the judge, change `judge_model()` in `evals/metrics.py` (see DeepEval's [model docs](https://deepeval.com/docs/metrics-introduction)).

## Extending

- **Add test cases:** add entries to `data/goldens.json`.
- **Add a metric:** write a new `GEval(...)` in `evals/metrics.py` and add it to `all_metrics()`.
- **Catch regressions:** change the system prompt in `app/support_bot.py` (for example, remove "Never invent prices") and rerun to see Groundedness drop.

## CI

`.github/workflows/eval.yml` runs the suite on every pull request. Add `ANTHROPIC_API_KEY` as a repository secret (**Settings → Secrets and variables → Actions**).

> Note: every eval run makes real API calls (5 app calls + several judge calls per metric), so it costs a small amount each time.

## License

MIT
