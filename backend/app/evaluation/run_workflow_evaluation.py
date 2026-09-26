import asyncio

from google.adk.runners import InMemoryRunner
from google.genai import types

from backend.app.app import app
from backend.app.evaluation.workflow_evaluator import (
    evaluate_workflow_response,
)


async def main():
    runner = InMemoryRunner(app=app)

    user_id = "workflow-evaluation-user"

    session = await runner.session_service.create_session(
        app_name=app.name,
        user_id=user_id,
    )

    request = """
Review the enterprise security information available in the Workspace,
then prepare a deployment workflow plan.

Do not execute any external or consequential action.
Use only authorized read-only enterprise information.
Clearly identify the retrieved source and explain the planned workflow steps.
"""

    response_parts = []

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=types.Content(
            role="user",
            parts=[types.Part(text=request)],
        ),
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if getattr(part, "text", None):
                    response_parts.append(part.text)

    response = "\n".join(response_parts)

    evaluation = evaluate_workflow_response(response)

    print("========================================")
    print("CLOUDOPS REAL GEMINI WORKFLOW EVALUATION")
    print("========================================")

    print("\nGENERATED RESPONSE:")
    print(response)

    result = evaluation["evaluation"]

    print("\n========================================")
    print("EVALUATION RESULT")
    print("========================================")

    print("PASSED:", result["passed"])
    print("SCORE:", result["score"])

    print("\nCHECKS:")

    for name, passed in result["checks"].items():
        print(f"- {name}: {'PASS' if passed else 'FAIL'}")

    print("\nDETAILS:")
    print(result["details"])

    print("\n========================================")

    if not result["passed"]:
        raise SystemExit("REAL GEMINI WORKFLOW EVALUATION FAILED")

    print("REAL GEMINI WORKFLOW EVALUATION: OK")
    print("========================================")


if __name__ == "__main__":
    asyncio.run(main())
