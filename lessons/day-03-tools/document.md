# Day 03: Tools

**One-line takeaway:** A tool is a Python function the model can *ask* you to run. The model never runs it. It sends a request, your code runs the function, and you send the result back.

---

## The ShopDesk scenario

Since Day 1, ShopDesk has been asked "where is order #1042?" and has never been able to answer. It had no way to look anything up.

Today it gets two tools:

| Tool | What it does |
|---|---|
| `get_order_status(order_id)` | Looks up an order and returns its status |
| `check_stock(product_name)` | Says how many units of a product are in stock |

(Both read from a small pretend database in `shared/shopdesk.py`.)

## The concept in plain words

Three terms, defined properly:

**Tool.** A normal Python function, plus a description the model can read: its name, its docstring, and its argument types. The model reads that description to decide *whether* and *how* to use the tool. The model cannot see or run your code.

**Tool call.** The model's *request* to use a tool: the tool's name, the arguments it wants to pass, and a unique id. It arrives inside the `AIMessage` (in `ai_msg.tool_calls`). When you see a tool call, **nothing has run yet.** It is a request waiting for you.

**ToolMessage.** The *result* of running the tool, wrapped as a message and sent back to the model. It carries the id of the tool call it answers, so the model can match request to result. The model reads it and writes the final reply to the customer.

```
 Customer: "Where is order #1042?"
      │
      ▼
 MODEL  ──►  AIMessage with a TOOL CALL: get_order_status(order_id="1042")
      │                         (a request, nothing has run)
      ▼
 YOUR CODE runs get_order_status("1042")
      │
      ▼
 ToolMessage: "Order 1042: ... In transit ... within 2 business days"
      │
      ▼
 MODEL  ──►  "Your shoes are in transit and should arrive within 2 days."
```

## Code walkthrough

Open [`lesson.py`](./lesson.py). It has two parts.

**The tools** are at the top. `@tool` turns a function into a tool. Notice the docstrings and type hints: they are the tool's instructions for the model.

**`main()`** has six numbered steps:

| # | What it shows |
|---|---|
| 1 | What the model sees about each tool: its name, description and argument types |
| 2 | A tool is just a function. We call it directly, no AI involved. |
| 3 | `model.bind_tools(tools)` tells the model which tools it may ask for. We print its tool call. |
| 4 | We run each requested tool ourselves: `tool.invoke(call)` returns a `ToolMessage`, which we append to the history |
| 5 | We invoke the model again with the full history; it writes the answer from the tool result |
| 6 | A message that needs no tool ("Thanks!"): the model just answers, and `tool_calls` is empty |

`shared/shopdesk.py` gains the order data, a new system prompt (the Day 2 one told ShopDesk it *couldn't* look things up, which is no longer true), and the "thanks" message.

## Run it

```bash
uv run python lessons/day-03-tools/lesson.py
```

## What you should see

Your exact words will differ. The shape:

```
=== 1. What the model sees ===
get_order_status: Look up the status of a customer's order.
   arguments: {'order_id': {'title': 'Order Id', 'type': 'string'}}
check_stock: Check how many units of a product are in stock.
   arguments: {'product_name': {'title': 'Product Name', 'type': 'string'}}

=== 2. Calling a tool directly (no model yet) ===
Order 1042: Trail Runner running shoes - In transit. Shipped with SwiftShip, ...
No order found with ID 9999.

=== 3. The model's tool call (a REQUEST, nothing has run yet) ===
name=get_order_status  args={'order_id': '1042'}  id=(a provider-generated id)

=== 4. Running the tools ourselves ===
ToolMessage -> Order 1042: Trail Runner running shoes - In transit. ...

=== 5. ShopDesk's final answer ===
(a short, friendly answer using the real status: in transit, within 2 business days)

=== 6. A message that needs no tool ===
tool calls: []
(a short "you're welcome")
```

> After you run it, paste your real output over this block. Steps 1, 2 and 4 are plain Python, so they should match exactly. Steps 3, 5 and 6 depend on the model.

## The gotcha

**The model never runs your function.** Beginners expect the model to "call the tool" the way code calls a function. It doesn't. It returns a *request*, and if your code doesn't run it and send the result back, nothing happens. That is the loop you wrote in steps 3 to 5.

More gotchas:
- **The docstring is a prompt.** "Look up the status of a customer's order" tells the model when to use the tool. A vague docstring ("Gets data") means the model uses the tool wrongly, or never. Type hints are required: they define the arguments the model is allowed to send.
- **Answer every tool call.** Each tool call needs a matching `ToolMessage` (same id) in the history before the next model call. Many providers reject a history where a request has no result. Using `tool.invoke(call)` handles the matching for you.
- **Return failures as text.** For an unknown order, the tool returns "No order found with ID 9999." instead of crashing. The model can then tell the customer politely.
- **Tools can have side effects.** Looking up an order is harmless. A tool that issues a refund is not, and the model might call it when it shouldn't. Approval steps for that come on **Day 19**.

## Try it yourself

1. Ask about order `1043` or `9999` by editing `CUSTOMER_MESSAGE`. What does the final answer say?
2. Ask "Do you have wool hiking socks, and where is order 1042?" The model may request **both tools at once** (parallel tool calls). Does your loop in step 4 handle it?
3. Make the `get_order_status` docstring vague ("Gets data"). Does the model still pick it?

## Why this matters for what comes next

This hand-written loop (ask, run, answer) is the core of every AI agent. A real agent just repeats it until the model stops asking for tools. **Day 6** shows the one-line prebuilt version, and **Day 10** builds the same loop yourself as a LangGraph graph with `ToolNode`.

⬅️ **Previous:** [Day 02, Messages](../day-02-messages/document.md)
➡️ **Next:** Day 04, Structured output

---

## LinkedIn post (copy, edit, post)

Day 3/30: my AI agent can finally look up an order. Here's the part that surprised me: the model never runs the code.

For two days, ShopDesk (my practice support agent) couldn't answer "where is order #1042?" Today it got tools.

Three terms, plainly:

→ Tool: a normal Python function plus a description the model can read: its name, docstring and argument types. The model can't see or run your code. It only reads the description to decide whether to use it.

→ Tool call: the model's request to use a tool. It has the tool's name, the arguments, and an id. Nothing has run yet. It's a request waiting for your code.

→ ToolMessage: the result of running the tool, sent back to the model with the same id. The model reads it and writes the final answer.

@tool
def get_order_status(order_id: str) -> str:
    """Look up the status of a customer's order."""
    ...

model_with_tools = model.bind_tools([get_order_status])
ai_msg = model_with_tools.invoke(messages)   # a request, not an answer

The loop you write: the model asks, your code runs the tool, you send back the result, the model answers.

Two things I'd have wanted to know earlier:
1. The docstring is a prompt. A vague one means the tool gets misused or ignored.
2. If a tool call gets no matching result, many providers reject the next request.

That loop is the heart of every AI agent. Day 10, I build it as a LangGraph graph.

Next: Day 4, structured output. (Day 1's chatbot ignored "output only the subject line." Time to fix that.)

Repo (bring your own API key): <link>

#LangChain #LangGraph #LangSmith #AIEngineering #Python
