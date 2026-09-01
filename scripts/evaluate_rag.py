"""
Runs the pipeline against tests/eval_dataset.json and stores pass/fail
results in the eval_results table.

Usage:
    python scripts/evaluate_rag.py
"""

import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.orchestrator.pipeline import run_pipeline
from app.db.database import SessionLocal
from app.db import crud

EVAL_PATH = os.path.join(os.path.dirname(__file__), "..", "tests", "eval_dataset.json")


def keyword_match(actual: str, expected: str) -> bool:
    """Very simple pass criterion: expected keywords appear in the answer.
    Swap this out for a stricter LLM-graded eval if you want."""
    actual_lower = actual.lower()
    return all(kw.lower() in actual_lower for kw in expected.split("|"))


def main():
    with open(EVAL_PATH) as f:
        eval_set = json.load(f)

    db = SessionLocal()
    passed_count = 0

    try:
        for item in eval_set:
            question = item["question"]
            expected = item.get("expected_keywords", "")

            result = run_pipeline(question, db=None)  # don't double-log to query_logs
            passed = keyword_match(result["answer"], expected) if expected else result["grounded"]
            passed_count += int(passed)

            crud.save_eval_result(
                db,
                question=question,
                expected=expected,
                actual=result["answer"],
                grounded=result["grounded"],
                passed=passed,
            )
            print(f"[{'PASS' if passed else 'FAIL'}] {question}")

        print(f"\n{passed_count}/{len(eval_set)} passed")
    finally:
        db.close()


if __name__ == "__main__":
    main()
