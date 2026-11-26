# Day 5: Your first LangSmith trace

> For four days ShopDesk could only show us what it *printed*. Today we turn on tracing and see what actually happened inside.

## The scenario

A customer says ShopDesk gave a wrong answer. Which messages were sent? Did a tool run? How long did it take? What did it cost? Printing everything with `print()` doesn't scale. A **trace** answers all of it.

## Three terms, plainly

- **Trace**: the full recorded story of one request, from the first input to the final output, with every step inside it, plus timing, token counts and errors.
- **Run**: one step inside a trace, such as a single model call or a single tool call. A trace is a tree of runs: the parent run contains its child runs.
- **Tags and metadata**: labels you attach to a trace so you can find it later. Tags are short strings (`"inbox"`); metadata is key-value facts (`"customer_tier": "gold"`).

## Setup (once)

1. **Account and key.** Make a free account at [smith.langchain.com](https://smith.langchain.com). Go to Settings and create an API key.
2. **Register an agent.** LangSmith now groups traces under an agent. In the UI, use **+ Agent**, then **Connect** > **Connect an existing agent**. Enter the name `shopdesk` and the Agent ID `shopdesk`. The ID can't be changed later. Choose the `local` environment.
3. **Fill in `.env`** (the template is in `.env.example`):

```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=<your key>
LANGSMITH_AGENT_ID=shopdesk
LANGSMITH_AGENT_ENVIRONMENT=local
```

4. **Not in the US region?** Also set `LANGSMITH_ENDPOINT` to your region's API URL (for example `https://eu.api.smith.langchain.com`).

The LangSmith UI changes from time to time. If a menu name differs, follow the current [LangSmith quickstart](https://docs.langchain.com/langsmith/observability-quickstart); the four environment variables above are the part that matters.

## The idea

Your code barely changes. LangChain sees the environment variables and records every model and tool call automatically:

```python
model.invoke(messages)                      # traced automatically

model.invoke(messages, config={             # same, but findable
    "run_name": "stock_question",
    "tags": ["day-05", "inbox"],
    "metadata": {"channel": "email", "customer_tier": "gold"},
})

@traceable(name="shopdesk_tool_loop")       # groups several steps into one trace
def answer_with_tools(question): ...
```

## What the lesson does

| Step | What happens | What to look for in LangSmith |
|---|---|---|
| 0 | Prints whether tracing is on (never prints your key) | Tells you what to fix if nothing shows up |
| 1 | One plain model call | Inputs, output, latency, token counts |
| 2 | Same kind of call with `run_name`, `tags`, `metadata` | A trace called `stock_question` that you can filter by tag |
| 3 | The Day 3 tool loop inside `@traceable` | One trace `shopdesk_tool_loop` with three children: model asks, tool runs, model answers |

## Run it

```bash
uv run python lessons/day-05-langsmith-trace/lesson.py
```

The lesson also runs with tracing off. It just tells you what is missing.

## What you should see

In your terminal, step 0 should read:

```text
LANGSMITH_TRACING          : on
LANGSMITH_API_KEY          : set
LANGSMITH_AGENT_ID         : shopdesk
LANGSMITH_AGENT_ENVIRONMENT: local
```

Then, in LangSmith under agent `shopdesk` > Tracing, open `shopdesk_tool_loop`. Add a screenshot of your own trace tree here; it is the best part of the post.

## Gotchas

1. **Both agent variables, or neither.** If only one of `LANGSMITH_AGENT_ID` and `LANGSMITH_AGENT_ENVIRONMENT` is set, the SDK logs a warning and sends nothing. That is the most likely reason for "I ran it and see nothing".
2. **Old project variables conflict.** Remove `LANGSMITH_PROJECT`, `LANGCHAIN_PROJECT` and `LANGCHAIN_SESSION` from your environment. They clash with agent addressing.
3. **Traces go out in the background.** A short script can exit before they are sent. The lesson calls `wait_for_all_tracers()` at the end so none are lost.
4. **Traces contain your real prompts and answers.** They are sent to LangSmith. Don't trace customer data you aren't allowed to send there. For production, check what your company allows before turning tracing on.
5. **Without `@traceable`, steps are separate traces.** Group the steps of one request under one parent so you can read the whole story in one place.
6. **Wrong region means the key is rejected.** A US-region default with an EU account looks like an authentication error.

## Try it yourself

- Break something: ask `answer_with_tools("Where is order #9999?")` and open the trace. The tool result says "No order found". Does the final answer match it?
- Filter your traces by the `day-05` tag, then by the `customer_tier` metadata.
- Find the token counts for step 1 and compare them with the `usage_metadata` you printed on Day 1.

## Where this goes next

Day 6 builds the same tool loop with `create_agent`, then adds middleware. You'll see it in the same trace view.

[← Day 4: Structured output](../day-04-structured-output/document.md) · Next: Day 6, `create_agent` and middleware

## LinkedIn post (copy and paste)

```text
Day 5/30: Your first LangSmith trace. Stop guessing what your agent did.

My support agent gave a wrong answer. All I had was what it printed. Which messages went in? Did the tool run? What did it cost? No idea.

Three terms, plainly:

→ Trace: the full recorded story of one request, from first input to final output, with timing, token counts and errors.

→ Run: one step inside a trace, like a single model call or tool call. A trace is a tree of runs.

→ Tags and metadata: labels you attach so you can find a trace later. Tags are short strings; metadata is key-value facts like customer_tier.

The best part: my code barely changed. Four environment variables turn it on:

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=...
LANGSMITH_AGENT_ID=shopdesk
LANGSMITH_AGENT_ENVIRONMENT=local

Then I wrapped the Day 3 tool loop in @traceable and got one trace with three children: the model asks, the tool runs, the model answers.

Things I'd have wanted to know earlier:
1. Set both agent variables, or nothing is sent (and you only get a warning).
2. Traces contain your real prompts. Don't send data you're not allowed to.
3. Group steps with @traceable, or one request becomes several traces.

Day 6: the same loop with create_agent.

Repo (bring your own API key): <link>

#LangChain #LangGraph #LangSmith #AIEngineering #Python
```
