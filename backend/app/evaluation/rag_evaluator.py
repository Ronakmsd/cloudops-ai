from typing import Any

from backend.app.evaluation.rag_eval_dataset import RAG_EVALUATION_DATASET
from backend.app.rag.tool import search_enterprise_knowledge


def concept_found(
    concept_variants: list[str],
    retrieved_text: str,
) -> bool:
    return any(
        variant.lower() in retrieved_text
        for variant in concept_variants
    )


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    result = search_enterprise_knowledge(
        query=case["question"],
        top_k=3,
    )

    if not result.get("success"):
        return {
            "id": case["id"],
            "question": case["question"],
            "passed": False,
            "score": 0.0,
            "matched_concepts": [],
            "missing_concepts": case["expected_concepts"],
            "retrieved_results": 0,
        }

    retrieved_text = " ".join(
        item["text"] for item in result.get("results", [])
    ).lower()

    expected = case["expected_concepts"]

    matched = []
    missing = []

    for variants in expected:
        if concept_found(variants, retrieved_text):
            matched.append(variants[0])
        else:
            missing.append(variants[0])

    score = len(matched) / len(expected) if expected else 0.0

    return {
        "id": case["id"],
        "question": case["question"],
        "passed": score == 1.0,
        "score": round(score, 4),
        "matched_concepts": matched,
        "missing_concepts": missing,
        "retrieved_results": len(result.get("results", [])),
    }


def evaluate_rag() -> dict[str, Any]:
    cases = [
        evaluate_case(case)
        for case in RAG_EVALUATION_DATASET
    ]

    overall_score = (
        sum(case["score"] for case in cases) / len(cases)
        if cases
        else 0.0
    )

    passed_cases = sum(
        1 for case in cases if case["passed"]
    )

    return {
        "total_cases": len(cases),
        "passed_cases": passed_cases,
        "failed_cases": len(cases) - passed_cases,
        "overall_score": round(overall_score, 4),
        "cases": cases,
    }


if __name__ == "__main__":
    result = evaluate_rag()

    print("========================================")
    print("CLOUDOPS AI RAG EVALUATION")
    print("========================================")

    print("TOTAL CASES:", result["total_cases"])
    print("PASSED:", result["passed_cases"])
    print("FAILED:", result["failed_cases"])
    print("OVERALL SCORE:", result["overall_score"])

    print("\nCASE RESULTS:")

    for case in result["cases"]:
        print(
            f'{case["id"]}: '
            f'score={case["score"]} '
            f'passed={case["passed"]} '
            f'retrieved={case["retrieved_results"]}'
        )

    print("\nRAG EVALUATION: COMPLETE")
