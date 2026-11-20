"""Standalone evaluation run (no pytest): prints a per-metric summary.

Usage:  python run_eval.py
"""

from deepeval import evaluate

from evals.dataset import build_test_case, load_goldens
from evals.metrics import all_metrics


def main() -> None:
    test_cases = [build_test_case(g) for g in load_goldens()]
    result = evaluate(test_cases=test_cases, metrics=all_metrics())

    print("\n=== Summary ===")
    totals: dict[str, list[float]] = {}
    passed = 0
    for tr in result.test_results:
        passed += tr.success
        for md in tr.metrics_data or []:
            totals.setdefault(md.name, []).append(md.score or 0.0)
    for name, scores in totals.items():
        print(f"{name:<30} avg score {sum(scores) / len(scores):.2f}")
    print(f"Test cases passed: {passed}/{len(result.test_results)}")


if __name__ == "__main__":
    main()
