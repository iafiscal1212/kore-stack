# kore-stack

Complete cognitive middleware stack for LLMs. One install, everything connected.

**Memory + Identity + Cache + Routing + Observability + A/B Testing.**

The difference with LangChain/LlamaIndex: kore's routing is based on formal proof complexity theory (Selector Complexity), not heuristics.

## Install

```bash
pip install kore-stack               # core (Ollama-ready)
pip install kore-stack[openai]       # + OpenAI
pip install kore-stack[anthropic]    # + Anthropic
pip install kore-stack[all]          # everything
```

## Quick start

```python
from kore_stack import Mind, Bridge, OllamaProvider

mind = Mind("agent.db")
llm = OllamaProvider(model="llama3.2")
bridge = Bridge(mind=mind, llm=llm, cache_ttl=3600.0)

response = bridge.think("Help me with my proof", user="carlos")
```

## What's new in v0.1.1

- `kore-mind>=0.3.1`: optimized Ollama embeddings — connection reuse, LRU cache, batch embedding (`embed.batch(texts)`), fallback warnings
- `kore-bridge>=0.3.1`: dependency bump

## What's in the stack

### kore-mind — Persistent memory engine
```python
from kore_stack import Mind

mind = Mind("agent.db", enable_traces=True)
mind.experience("User likes Python", source="carlos")
memories = mind.recall("Python", source="carlos")

# Scoped views per user
alice = mind.scoped("alice")
alice.experience("Prefers Rust")
```

### kore-bridge — LLM cognitive middleware
```python
from kore_stack import Bridge, OllamaProvider

bridge = Bridge(
    mind=mind,
    llm=OllamaProvider(),
    cache_ttl=3600.0,    # smart cache
    rate_limit=3,         # cognitive rate limiting
    rate_window=3600.0,
)

# Cache hit → no LLM call. Rate limited → respond from memory.
response = bridge.think("What is P vs NP?", user="carlos")
```

### sc-router — Routing based on Selector Complexity
```python
from kore_stack import (
    SCRouterProvider, ToolCatalog, Tool,
    OllamaProvider, Bridge, Mind,
)
from kore_bridge.providers import OpenAIProvider

# Define your tool catalog
catalog = ToolCatalog()
catalog.register(Tool(
    name="calculator",
    description="Arithmetic calculations",
    input_types={"expression"},
    output_types={"number"},
    capability_tags={"math", "calculate"},
))

# SC routing: simple queries → local Ollama, complex → GPT-4
router = SCRouterProvider(
    providers={
        "fast": OllamaProvider(model="llama3.2"),
        "quality": OpenAIProvider(model="gpt-4o"),
    },
    catalog=catalog,
)

bridge = Bridge(mind=Mind("agent.db"), llm=router)
bridge.think("What is 2+2?")        # SC(0) → Ollama
bridge.think("Analyze market trends, cross-reference sentiment, build prediction model")
                                      # SC(2-3) → GPT-4
print(router.last_sc_level)          # 0, 1, 2, or 3
```

### A/B Testing
```python
from kore_stack import Experiment, OllamaProvider, Mind

exp = Experiment(
    Mind("test.db"),
    variant_a=OllamaProvider(model="llama3.2"),
    variant_b=OllamaProvider(model="mistral"),
)

result = exp.run("Explain recursion")
print(f"A: {result.time_a_ms:.0f}ms, B: {result.time_b_ms:.0f}ms, faster: {result.faster}")
```

## Architecture

```
┌─────────────┐
│   Your App  │
└──────┬──────┘
       │
┌──────▼──────┐
│ kore-bridge │  Cache → Rate Limit → SC Route → LLM
│  (Bridge)   │
└──────┬──────┘
       │
┌──────▼──────┐     ┌───────────┐
│  kore-mind  │     │ sc-router │
│   (Mind)    │     │  SC(0-3)  │
│   SQLite    │     └───────────┘
└─────────────┘
```

## Packages

| Package | PyPI | What it does |
|---------|------|-------------|
| [kore-mind](https://github.com/iafiscal1212/kore-mind) | `pip install kore-mind` | Memory, identity, traces, cache storage |
| [kore-bridge](https://github.com/iafiscal1212/kore-bridge) | `pip install kore-bridge` | LLM integration, cache logic, rate limiting, A/B |
| [sc-router](https://github.com/iafiscal1212/sc-router) | `pip install sc-router` | Query routing by Selector Complexity |
| **kore-stack** | `pip install kore-stack` | **All of the above, one install** |

## License

MIT
