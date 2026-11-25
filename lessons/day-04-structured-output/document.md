# Day 4: Structured output

> ShopDesk's inbox is full of messy messages. Today the model turns each one into a tidy **ticket** your code can act on.

## The scenario

| Customer writes | We need |
|---|---|
| "URGENT!! Order #1042 was due Friday... I want a refund and a manager." | `category=refund`, `urgency=high`, `order_id="1042"`, `needs_human=True` |
| "Are the wool hiking socks back in stock? No rush." | `category=product_question`, `urgency=low`, `order_id=None` |

A paragraph of text can't be routed by an `if` statement. An object with fields can.

## Three terms, plainly

- **Structured output**: asking the model to reply with data that matches a shape you define, instead of free text. You get back an object, not a string.
- **Schema**: the definition of that shape: field names, types, allowed values and a description of each. We write it as a Pydantic class.
- **Validation**: checking that data really matches the schema (right types, allowed values only). Pydantic does this for you and raises an error when it doesn't.

## The idea in four lines

```python
class Ticket(BaseModel):
    category: Literal["order_status", "refund", "product_question", "complaint", "other"]
    urgency: Literal["low", "medium", "high"]
    ...

triage_model = model.with_structured_output(Ticket)
ticket = triage_model.invoke(messages)   # a Ticket object, not an AIMessage
if ticket.needs_human or ticket.urgency == "high": ...
```

## What the lesson does

| Step | What happens | Why it matters |
|---|---|---|
| 1 | Ask for JSON in plain text, then `json.loads` it | Shows why this is fragile: extra words or code fences break parsing |
| 2 | `with_structured_output(Ticket)` | The reply is a `Ticket` object with typed fields |
| 3 | Route both messages with `if/else`, then `model_dump()` | Fields are just Python attributes; `model_dump()` gives a dict for JSON or a database |
| 4 | `include_raw=True` | Returns `raw` (the AIMessage), `parsed` (the Ticket) and `parsing_error`, so you keep token counts and can handle failures |
| 5 | Build `Ticket(category="banana", ...)` by hand | Pydantic raises `ValidationError`: only the allowed values pass |

## Run it

```bash
uv run python lessons/day-04-structured-output/lesson.py
```

## What you should see

This is the shape of the output. Your wording will differ, so replace this block with your real run.

```text
=== 1. Asking for JSON in plain text ===
-> json.loads FAILED (...)     # or "worked this time": it is not guaranteed

=== 2. with_structured_output(Ticket) ===
type: Ticket
category: refund
urgency: high
order_id: 1042
needs_human: True
summary: Order #1042 is late and the customer wants a refund and a manager.

=== 3. Route both messages with plain if/else ===
- [  high] refund           -> ESCALATE to a human
- [   low] product_question -> auto-reply from the product catalog

=== 5. Bad data is rejected ===
ValidationError on 'category': Input should be 'order_status', 'refund', ...
```

## Gotchas

1. **The schema is a prompt.** Field names, the class docstring and every `description=` are sent to the model. A vague description gives vague results, just like a vague tool docstring on Day 3.
2. **Use `Literal` for fixed choices.** Without it, the model may invent `"Refund"`, `"refunds"` or `"money back"`, and your `if` statements stop matching.
3. **Mark missing data as optional.** `order_id: str | None` lets the model say "none". A required field with no answer pushes the model to make something up.
4. **Provider support differs.** Some providers enforce the schema natively; others force a tool call behind the scenes. Your code looks the same, but `method=` lets you choose. Check your provider's page if results look odd.
5. **Pydantic checks shape, not truth.** A `Ticket` can be perfectly valid and still wrong (the model may pick the wrong category). Validation catches broken data, not bad judgment. Evals (Week 3) catch that.
6. **A model can refuse.** For these cases, `include_raw=True` lets you inspect `parsing_error` instead of crashing.

## Try it yourself

- Add a `"shipping_address_change"` category and re-run. Does the model use it for Day 2's "send it to my office"?
- Add `sentiment: Literal["calm", "frustrated", "angry"]`. Watch how its `description` changes the answer.
- Make `order_id` required (remove `| None`) and run the socks message. What does the model put there?

## Where this goes next

The ticket is ShopDesk's first piece of real data. On Day 7 it becomes part of a LangGraph **state**, so every node in the graph can read it.

[← Day 3: Tools](../day-03-tools/document.md) · Next: Day 5, your first LangSmith trace

## LinkedIn post (copy and paste)

```text
Day 4/30: Structured output. Stop parsing paragraphs.

My support agent used to answer "URGENT!! my order is late, I want a manager" with a nice paragraph. Great for a person. Useless for code.

Three terms, plainly:

→ Structured output: asking the model to reply with data in a shape you define, so you get an object back instead of a string.

→ Schema: that shape: field names, types, allowed values and a description of each. In Python it's a Pydantic class.

→ Validation: checking the data really matches the schema. Pydantic rejects anything outside it.

Now the same message becomes:
category=refund, urgency=high, order_id="1042", needs_human=True

And routing is just an if statement.

ticket = model.with_structured_output(Ticket).invoke(messages)

Things I'd have wanted to know earlier:
1. The schema is a prompt. Field descriptions steer the model.
2. Use Literal for fixed choices, or the model invents its own labels.
3. Valid is not the same as correct. Pydantic checks shape, not judgment.

Day 7, this ticket becomes LangGraph state.

Repo (bring your own API key): <link>

#LangChain #LangGraph #LangSmith #AIEngineering #Python
```
