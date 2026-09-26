from google.adk.apps import App
from google.adk.agents.context_cache_config import ContextCacheConfig

from backend.app.agents.agent import root_agent


app = App(
    name="cloudops_ai",
    root_agent=root_agent,
    context_cache_config=ContextCacheConfig(
        cache_intervals=10,
        ttl_seconds=1800,
        min_tokens=2048,
    ),
)

print("CLOUDOPS AI APP: CONTEXT CACHE ENABLED")
