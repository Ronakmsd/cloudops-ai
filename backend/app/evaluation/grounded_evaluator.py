from typing import Any

from google.genai import types

from backend.app.evaluation.grounded_eval_dataset import (
    GROUNDED_EVALUATION_DATASET,
)
from backend.app.runtime.runner import create_runner


def fact_found(
    fact_variants: list[str],
    answer: str,
) -> bool:
    normalized = answer.lower()

    return any(
        variant.lower() in normalized
        for variant in fact_variants
    )


async def generate_answer(
    runner,
    question: str,
    user_id: str,
    session_id: str,
) -> str:
    message = types.Content(
        role="user",
        parts=[types.Part(text=question)],
    )

    final_text = ""

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_text = event.content.parts[0].text

    return final_text


async def evaluate_case(
    runner,
    case: dict[str, Any],
    index: int,
) -> dict[str, Any]:

    user_id = f"grounded_eval_user_{index}"

    session = await runner.session_service.create_session(
        app_name="cloudops_ai",
        user_id=user_id,
    )

    answer = await generate_answer(
        runner=runner,
        question=case["question"],
        user_id=user_id,
        session_id=session.id,
    )

    required_facts = case["required_facts"]

    matched = []
    missing = []

    for variants in required_facts:
        if fact_found(variants, answer):
            matched.append(variants[0])
        else:
            missing.append(variants[0])

    score = (
        len(matched) / len(required_facts)
        if required_facts
        else 0.0
    )

    return {
        "id": case["id"],
        "question": case["question"],
        "score": round(score, 4),
        "passed": score == 1.0,
        "matched_facts": matched,
        "missing_facts": missing,
        "answer": answer,
    }


async def evaluate_groundedness() -> dict[str, Any]:
    runner = create_runner()

    cases = []

    for index, case in enumerate(
        GROUNDED_EVALUATION_DATASET,
        start=1,
    ):
        result = await evaluate_case(
            runner,
            case,
            index,
        )

        cases.append(result)

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
    import asyncio

    result = asyncio.run(
        evaluate_groundedness()
    )

    print("========================================")
    print("CLOUDOPS AI GROUNDEDNESS EVALUATION")
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
            f'passed={case["passed"]}'
        )

        if case["missing_facts"]:
            print(
                "  MISSING:",
                case["missing_facts"],
            )

    print("\nGROUNDEDNESS EVALUATION: COMPLETE")
