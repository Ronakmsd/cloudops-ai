from google.adk.runners import InMemoryRunner

from backend.app.app import app


def create_runner() -> InMemoryRunner:
    """
    Create the CloudOps AI runner from the configured App.

    The App owns the root agent and application-wide settings,
    including context caching.
    """

    return InMemoryRunner(
        app=app,
    )
