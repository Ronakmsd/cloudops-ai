from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class WorkflowStep:
    step_id: int
    action: str
    description: str
    requires_confirmation: bool


@dataclass(frozen=True)
class WorkflowPlan:
    objective: str
    status: str
    steps: list[WorkflowStep]
    execution_mode: str


def create_workflow_plan(
    objective: str,
    *,
    execution_mode: str = "plan_only",
) -> dict[str, Any]:
    """
    Create a safe, non-executing enterprise workflow plan.

    The planner describes intended actions but does not perform
    external side effects.
    """

    objective = objective.strip()

    if not objective:
        raise ValueError("Workflow objective cannot be empty.")

    if execution_mode not in {
        "plan_only",
        "requires_confirmation",
    }:
        raise ValueError(
            "Unsupported execution mode."
        )

    steps = [
        WorkflowStep(
            step_id=1,
            action="understand_request",
            description=(
                "Understand the requested business objective "
                "and identify the required enterprise information."
            ),
            requires_confirmation=False,
        ),
        WorkflowStep(
            step_id=2,
            action="retrieve_information",
            description=(
                "Retrieve relevant information using authorized "
                "read-only enterprise tools."
            ),
            requires_confirmation=False,
        ),
        WorkflowStep(
            step_id=3,
            action="validate_results",
            description=(
                "Validate retrieved information, source provenance "
                "and applicable authorization constraints."
            ),
            requires_confirmation=False,
        ),
        WorkflowStep(
            step_id=4,
            action="prepare_next_action",
            description=(
                "Prepare the next workflow action without executing "
                "any consequential external operation."
            ),
            requires_confirmation=True,
        ),
    ]

    plan = WorkflowPlan(
        objective=objective,
        status="planned",
        steps=steps,
        execution_mode=execution_mode,
    )

    return {
        "success": True,
        "workflow": asdict(plan),
        "side_effects": False,
    }
