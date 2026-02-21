"""kore-stack: Complete cognitive middleware stack for LLMs.

One install, everything connected:
    pip install kore-stack

Includes:
    - kore-mind: Persistent memory + emergent identity
    - kore-bridge: LLM integration with cache, rate limiting, A/B testing
    - sc-router: Query routing based on Selector Complexity theory
"""

# Re-export everything for convenience
from kore_mind import Mind, Memory, Identity, MemoryType, Trace, CacheEntry
from kore_bridge import (
    Bridge, LLMProvider, CallableLLM, OllamaProvider,
    RouterProvider, SCRouterProvider, Experiment, ExperimentResult,
)
from sc_router import ToolCatalog, Tool, route

__version__ = "0.1.0"
__all__ = [
    # Mind
    "Mind", "Memory", "Identity", "MemoryType", "Trace", "CacheEntry",
    # Bridge
    "Bridge", "LLMProvider", "CallableLLM", "OllamaProvider",
    "RouterProvider", "SCRouterProvider", "Experiment", "ExperimentResult",
    # SC Router
    "ToolCatalog", "Tool", "route",
]
