# Day 01: Chat Models

**One-line takeaway:** `init_chat_model("provider:model")` gives you a model object, `.invoke()` sends a prompt, and what comes back is an `AIMessage`, not a string.

---

## The ShopDesk scenario

ShopDesk is a make-believe online store. A customer writes in:

> "Hi! I ordered a pair of running shoes last week (order #1042) and it still hasn't arrived. Can you tell me where it is?"

Today ShopDesk does the simplest possible thing: it sends that message to a chat model and prints the reply. Every later lesson adds one skill on top of this.

## The concept in plain words

A **chat model** is the AI brain. You give it text, it gives text back. LangChain wraps every provider (OpenAI, Anthropic, Google, and more) in the *same* interface, so your code does not change when the provider does.

```
your prompt  ──►  model.invoke()  ──►  AIMessage
                                         ├─ .text            the reply
                                         ├─ .usage_metadata  token counts
                                         └─ .response_metadata  provider extras
```

Three things to remember:

1. **`init_chat_model`** builds the model. You pass `"provider:model-name"`, for example `openai:gpt-5.4-mini`. Swap the string and you have swapped the provider.
2. **`invoke`** sends the prompt and waits for the full reply.
3. **Settings** such as `temperature` (steady vs. varied answers) and `max_tokens` (maximum reply length) are passed when you build the model.

## Code walkthrough

Open [`lesson.py`](./lesson.py). It has five numbered sections:

| # | What it shows |
|---|---|
| 1 | `init_chat_model(model_name)` builds the model from the name in your `.env` |
| 2 | `model.invoke(prompt)` sends the customer's message |
| 3 | The response is an `AIMessage`; we print its type and `usage_metadata` |
| 4 | Run the same prompt at `temperature=0` and `temperature=1`, twice each |
| 5 | `max_tokens=30` cuts the reply short, which also caps the cost |

The helper `shared/config.py` reads your `.env` and checks your key is filled in, so you get a clear message instead of a stack trace if something is missing.

## Run it

From the repo root, after the setup steps in the main [README](../../README.md):

```bash
uv run python lessons/day-01-chat-models/lesson.py
```

## What you should see

Your exact words will differ, because models are not deterministic. The shape is:

```
=== 2. ShopDesk's reply ===
(a short, polite reply that apologises and asks for more details,
 or says it cannot see order #1042)

=== 3. What is inside the response ===
type   : AIMessage
tokens : {'input_tokens': ..., 'output_tokens': ..., 'total_tokens': ...}

=== 4. temperature ===
temperature=0 run 1: (a subject line)
temperature=0 run 2: (usually the same or very close)
temperature=1 run 1: (a subject line)
temperature=1 run 2: (usually different wording)

=== 5. max_tokens ===
(a reply that stops mid-sentence)
output tokens: ~30
```

## The gotcha

**`invoke` returns an `AIMessage`, not a string.** `print(response)` shows the whole object with metadata. Use `response.text` for the words.

You may also see `response.content`. For some providers that is a *list of content blocks* rather than a string, and `.text` is the safe way to get plain text.

Two smaller ones:
- Not every model accepts a custom `temperature`. The lesson catches that and prints a hint instead of crashing.
- A reply cut off by `max_tokens` stops mid-sentence. It is a hard limit, not a polite suggestion to the model.

## Try it yourself

1. Change `MODEL_NAME` in `.env` to another provider (and add its key). Rerun with **no code changes**.
2. Change the prompt so ShopDesk answers in a different language.
3. Set `max_tokens` to `5`. What happens to the reply?

## Why this matters for what comes next

Look at ShopDesk's reply. It cannot actually know where order #1042 is, because it has no way to look it up. The model only knows what is in the prompt. Fixing that is **Day 3 (Tools)**.

Also notice that the instructions and the customer message are mashed into one string. That is fragile. **Day 2 (Messages)** shows the proper way.

➡️ **Next:** Day 02, Messages

---

## LinkedIn post (copy, edit, post)

**Day 1/30: LangChain, LangGraph and LangSmith 🧱**

Starting a 30-day series: one runnable lesson a day, all in one GitHub repo.

Today: chat models, with a store support agent called ShopDesk.

```python
model = init_chat_model("openai:gpt-5.4-mini")
reply = model.invoke("Where is my order #1042?")
print(reply.text)
```

3 things I learned:
→ One line builds a model for any provider. Change the string, not the code.
→ `invoke` returns an `AIMessage`, not a string. Use `.text` for the words.
→ `temperature` and `max_tokens` control how varied and how long the reply is.

The fun part: ShopDesk can't actually know where order #1042 is. It has no tools yet. That's Day 3.

Repo + setup steps (bring your own API key): <link>

#LangChain #LangGraph #LangSmith #AIEngineering #Python
