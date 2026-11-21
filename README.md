# langchain-magic ✨

**30 days of LangChain, LangGraph and LangSmith.** One small, runnable Python lesson per day, all following one story: **ShopDesk**, an online store's AI support agent that gets a little smarter every day.

Each lesson is a folder with two files:

```
lessons/day-01-chat-models/
├── lesson.py      # the runnable example
└── document.md    # the explanation, gotchas, and a ready-to-post LinkedIn summary
```

## Setup (about 5 minutes)

You bring your own API key. Nothing is shared and nothing is stored in this repo.

**1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)** (a fast Python package manager). Python 3.10 or newer is needed.

**2. Clone the repo and install the dependencies.** Pick the provider you have a key for:

```bash
git clone <this-repo-url>
cd langchain-magic
uv sync --extra openai       # or: --extra anthropic   or: --extra google
```

Prefer plain `pip`? Create a virtual environment, open `requirements.txt`, uncomment the one provider line you need, then run:

```bash
python3 -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt```

(With `pip`, run lessons as `python lessons/day-01-chat-models/lesson.py`. With `uv`, use `uv run python ...` as shown below.)

**3. Create your `.env` file** from the template:

```bash
cp .env.example .env         # Windows (cmd): copy .env.example .env
```

Open `.env` and:
- set `MODEL_NAME` to a model from your provider, in `provider:model-name` format
- paste **your own** API key for that provider, and leave the other placeholders alone

`.env` is in `.gitignore`, so your keys never get committed.

**4. Run Day 1:**

```bash
uv run python lessons/day-01-chat-models/lesson.py
```

If something is missing, the lesson tells you exactly what to fix.

From Day 5 onward we also use **LangSmith** for tracing. Create a free account at [smith.langchain.com](https://smith.langchain.com), make an API key, and put it in `.env`. Keep `LANGSMITH_TRACING=false` until then.

## The 30-day plan

| Week | Theme | Days |
|---|---|---|
| 1 | LangChain essentials | 1 Chat models · 2 Messages · 3 Tools · 4 Structured output · 5 First LangSmith trace · 6 `create_agent` and middleware |
| 2 | LangGraph core | 7 State and reducers · 8 Routing · 9 `Command` and loops · 10 ReAct agent with `ToolNode` · 11 Parallel work (Send) · 12 Evaluator-optimizer loop |
| 3 | Persistence and memory | 13 Checkpointers and threads · 14 Durable checkpointer · 15 Trimming and summarization · 16 Long-term memory (store) · 17 Semantic search store · 18 Time travel |
| 4 | Human-in-the-loop, multi-agent, streaming | 19 `interrupt()` approvals · 20 Edit/reject, retries, idempotency · 21 Subgraphs · 22 Supervisor · 23 Stream modes · 24 Custom events |
| 5 | Guardrails, evals, production | 25 Guardrails · 26 Datasets and offline evals · 27 Online evals and feedback · 28 Testing graphs · 29 Deploying · 30 Capstone |


