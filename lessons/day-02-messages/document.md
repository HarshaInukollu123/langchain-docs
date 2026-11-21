# Day 02: Messages

**One-line takeaway:** A conversation is just a list of messages (system, human, AI). The model has no memory, so to continue a conversation you resend the list.

---

## The ShopDesk scenario

On [Day 1](../day-01-chat-models/document.md), ShopDesk replied "I'll check your order and get back to you." It can't do that. We also mashed the instructions and the customer's words into one string.

Today we fix both with **messages**, then handle a follow-up question from the customer:

> Customer: "Thanks. Could you send it to my office address instead?"

Say "it" to someone who never heard the first message, and they have no idea what you mean. That's exactly what happens to the model.

## The concept in plain words

Chat models do not take one blob of text. They take a **list of messages**, each with a role:

| Message | Role | What it is |
|---|---|---|
| `SystemMessage` | `system` | Standing instructions: who the model is and what rules to follow |
| `HumanMessage` | `human` | What the customer said |
| `AIMessage` | `ai` | What the model said (the reply from `invoke` is one) |

```
[ SystemMessage  ]   "You are ShopDesk. Never promise to check orders."
[ HumanMessage   ]   "Where is order #1042?"
[ AIMessage      ]   "I can't look up orders yet, but..."
[ HumanMessage   ]   "Send it to my office instead."   ◄── only makes sense with the lines above
```

The key idea: **the model is stateless.** Every `invoke` call starts from zero. It only knows what is in the list you send *this time*. A "conversation" is you keeping that list, adding to it, and sending the whole thing again.

## Code walkthrough

Open [`lesson.py`](./lesson.py). Five numbered sections:

| # | What it shows |
|---|---|
| 1 | `[SystemMessage(...), HumanMessage(...)]` passed to `invoke`. The system message stops the fake promise. |
| 2 | The reply is an `AIMessage`, with role `ai` |
| 3 | The follow-up sent **alone**. The model doesn't know what "it" is. |
| 4 | The follow-up sent **with the history**: `messages.append(reply)`, then append the new `HumanMessage`, then invoke again |
| 5 | Plain dicts (`{"role": "user", "content": "..."}`) work as messages too |

The `shared/shopdesk.py` file now holds ShopDesk's `SYSTEM_PROMPT` and the follow-up text, so every later lesson reuses them.

## Run it

```bash
uv run python lessons/day-02-messages/lesson.py
```

## What you should see

Your exact words will differ. The shape:

```
=== 1. ShopDesk's reply (compare with Day 1: no more fake promises) ===
(a short reply that does NOT promise to check the order, and asks for details)

=== 2. The reply is an AIMessage ===
is an AIMessage: True | role: ai

=== 3. Follow-up WITHOUT history (the model has no idea what 'it' is) ===
customer: Thanks. Could you send it to my office address instead?
ShopDesk: (confused: asks what "it" is, or which order you mean)

=== 4. Follow-up WITH history (we resent the whole conversation) ===
  system| You are ShopDesk, a friendly support agent for an online store. Reply ...
  human | Hi! I ordered a pair of running shoes last week (order #1042) and it ...
  ai    | (the reply from step 1)
  human | Thanks. Could you send it to my office address instead?
ShopDesk: (understands "it" = the shoes, and answers in context)

=== 5. Same first message, written as dicts ===
(a reply very similar to step 1)
```

> After you run it, paste your real output over this block, like we did on Day 1. Real output makes a better post.

## The gotcha

**The model remembers nothing between calls.** If you send only the new message, it answers as if the earlier conversation never happened. Beginners often assume a chat model "keeps the thread" the way ChatGPT's website does. The website resends the history for you. In code, that's your job.

Two smaller ones:
- **History grows with every turn.** You pay for all of it on every call, and long chats eventually hit the model's size limit. Managing that (trimming, summarizing) is **Day 15**.
- **The system message steers, but doesn't guarantee.** It reduced the fake promises, it didn't make them impossible. Real guardrails come in Week 5.

## Try it yourself

1. Delete the line `messages.append(reply)` and rerun. What does the model say now? (The conversation has a hole where ShopDesk's answer should be.)
2. Add a second follow-up: "Actually, can you also gift wrap it?" Append it and resend the list.
3. Change the system prompt so ShopDesk answers in a pirate voice. Which messages still follow the new rule?

## Why this matters for what comes next

Everything in LangGraph is built on this: **graph state is largely a list of messages** that nodes read and add to. When we reach Day 7, you'll recognize that `messages.append(...)` pattern, and LangGraph will do it for you.

ShopDesk is now honest, but it still can't actually look anything up. **Day 3 (Tools)** changes that.

⬅️ **Previous:** [Day 01, Chat models](../day-01-chat-models/document.md)
➡️ **Next:** Day 03, Tools

---

## LinkedIn post (copy, edit, post)

**Day 2/30: LangChain, LangGraph and LangSmith 💬**

Yesterday my support agent promised to "check your order." It can't. Today I fixed that, and learned something that surprised me.

A conversation with an LLM is just a list of messages:

```python
messages = [
    SystemMessage("You are ShopDesk. Never promise to check orders."),
    HumanMessage("Where is order #1042?"),
]
reply = model.invoke(messages)
```

→ SystemMessage = the rules
→ HumanMessage = the customer
→ AIMessage = the model's reply

The surprise: **the model remembers nothing.**

When the customer followed up with "Could you send it to my office instead?", I sent only that message. The model had no idea what "it" was.

The fix: keep the list, append the reply, append the new message, and send the whole thing again. "Memory" in code is just you resending history.

(Paste what the model said without history here. That's your hook.)

That's also why long chats get expensive: you pay for the whole list every call.

Next: Day 3, tools. ShopDesk is honest now. Time to make it useful.

Repo (bring your own API key): <link>

#LangChain #LangGraph #LangSmith #AIEngineering #Python
