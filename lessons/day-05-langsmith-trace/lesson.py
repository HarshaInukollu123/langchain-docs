"""Day 05 - Your first LangSmith trace: see what the model actually did.

ShopDesk scenario
-----------------
ShopDesk has been answering customers for four days, but we only see what it
PRINTS. When an answer is wrong, we cannot see what was sent, which tool ran,
how long it took or what it cost. Today we turn on tracing and look inside.

What you will learn
-------------------
1. Tracing is switched on with environment variables. No code changes.
2. One model call = one trace (inputs, output, time, tokens)
3. Names, tags and metadata - so you can find a trace later
4. @traceable - group several steps (model, tool, model) into ONE trace tree

Setup (once; full steps in document.md)
---------------------------------------
    1. Make a free account at smith.langchain.com and create an API key.
    2. In LangSmith, register an agent called "shopdesk" (Agent ID: shopdesk).
    3. In .env set LANGSMITH_TRACING=true and paste your LANGSMITH_API_KEY.

Run it (from the repo root)
---------------------------
    uv run python lessons/day-05-langsmith-trace/lesson.py
"""

import os

from langchain.messages import HumanMessage, SystemMessage
from langchain.tools import tool
from langchain_core.tracers.langchain import wait_for_all_tracers
from langsmith import traceable

from shared.config import get_model
from shared.shopdesk import (
    CUSTOMER_MESSAGE,
    INBOX_MESSAGES,
    ORDERS,
    SYSTEM_PROMPT,
    TOOLS_SYSTEM_PROMPT,
)


# The same order tool as Day 3, shortened. (Each lesson folder stands alone.)
@tool
def get_order_status(order_id: str) -> str:
    """Look up the status of a customer's order by its order number."""
    order = ORDERS.get(order_id.strip().lstrip("#"))
    if order is None:
        return f"No order found with ID {order_id}."
    return f"Order {order_id}: {order['item']} - {order['status']}. {order['detail']}"


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def tracing_is_ready() -> bool:
    """Say whether traces will be sent. Never prints your key."""
    on = os.getenv("LANGSMITH_TRACING", "").lower() in ("true", "1")
    key = os.getenv("LANGSMITH_API_KEY", "")
    agent = os.getenv("LANGSMITH_AGENT_ID")
    env = os.getenv("LANGSMITH_AGENT_ENVIRONMENT")
    print("LANGSMITH_TRACING          :", "on" if on else "off")
    print(
        "LANGSMITH_API_KEY          :",
        "set" if key and not key.startswith("your-") else "MISSING",
    )
    print("LANGSMITH_AGENT_ID         :", agent or "MISSING")
    print("LANGSMITH_AGENT_ENVIRONMENT:", env or "MISSING")
    return bool(on and key and not key.startswith("your-") and agent and env)


# ---- A parent "run" that groups the whole tool loop into ONE trace ----------
# Without @traceable, the two model calls and the tool call would show up as
# separate traces. With it, they are children of one parent you can open.
@traceable(name="shopdesk_tool_loop", tags=["day-05"], metadata={"lesson": "day-05"})
def answer_with_tools(question: str) -> str:
    model = get_model().bind_tools([get_order_status])
    messages = [SystemMessage(TOOLS_SYSTEM_PROMPT), HumanMessage(question)]

    ai_msg = model.invoke(messages)  # child run 1: the model asks for a tool
    if not ai_msg.tool_calls:
        return ai_msg.text
    messages.append(ai_msg)
    for call in ai_msg.tool_calls:
        messages.append(get_order_status.invoke(call))  # child run 2: the tool
    return model.invoke(messages).text  # child run 3: the final answer


def main() -> None:
    model = get_model()  # also loads your .env

    section("0. Is tracing on?")
    ready = tracing_is_ready()
    if not ready:
        print(
            "\nTracing is not fully set up, so nothing will be sent to LangSmith.\n"
            "The lesson still runs. See document.md, 'Setup', then run it again."
        )

    # 1. Nothing special in the code: the env vars do the work ----------------
    section("1. One plain model call")
    reply = model.invoke([SystemMessage(SYSTEM_PROMPT), HumanMessage(CUSTOMER_MESSAGE)])
    print(reply.text)

    # 2. Name it, tag it, attach facts so you can find it later -----------------
    section("2. Same kind of call, with a name, tags and metadata")
    reply = model.invoke(
        [SystemMessage(SYSTEM_PROMPT), HumanMessage(INBOX_MESSAGES[1])],
        config={
            "run_name": "stock_question",
            "tags": ["day-05", "inbox"],
            "metadata": {"channel": "email", "customer_tier": "gold"},
        },
    )
    print(reply.text)

    # 3. A whole tool loop as one trace tree ----------------------------------
    section("3. The Day 3 tool loop as ONE trace")
    print(answer_with_tools(CUSTOMER_MESSAGE))

    # Traces are sent in the background. Wait so none are lost when we exit.
    wait_for_all_tracers()

    section("Now open LangSmith")
    if ready:
        print("Open smith.langchain.com -> agent 'shopdesk' -> Tracing. Look for:")
        print(
            "  - a trace named 'shopdesk_tool_loop' (click it: you will see 3 children)"
        )
        print("  - a trace named 'stock_question' (check its tags and metadata)")
        print("  - the first plain call (check latency and token counts)")
    else:
        print("Turn tracing on, run again, then open smith.langchain.com.")

    print("\nDay 6 builds the same loop with create_agent, then adds middleware.")


if __name__ == "__main__":
    main()
