"""Day 03 - Tools: letting the model ask your code to do things.

ShopDesk scenario
-----------------
Since Day 1, ShopDesk could not actually look up order #1042. Today it gets two
tools: one to check an order's status, one to check stock. The model decides
WHEN to use them. Your code does the actual work.

What you will learn
-------------------
1. @tool        - turn a normal Python function into a tool
2. What the model reads: the tool's name, docstring and argument types
3. bind_tools   - tell the model which tools it is allowed to ask for
4. A tool call  - the model's REQUEST (nothing has run yet!)
5. ToolMessage  - the result you send back so the model can answer
6. The model may also choose NOT to use a tool

Run it (from the repo root, after setting up .env - see the README)
-------------------------------------------------------------------
    uv run python lessons/day-03-tools/lesson.py
"""

from langchain.messages import HumanMessage, SystemMessage
from langchain.tools import tool

from shared.config import get_model
from shared.shopdesk import (
    CUSTOMER_MESSAGE,
    ORDERS,
    STOCK,
    THANKS_MESSAGE,
    TOOLS_SYSTEM_PROMPT,
)


# ---- A tool is a normal function + a description the model can read ---------
# The name, the docstring and the type hints are what the model sees.
# Write the docstring for the MODEL: say what the tool does and when to use it.
@tool
def get_order_status(order_id: str) -> str:
    """Look up the status of a customer's order.

    Args:
        order_id: The order number, for example "1042" (a leading # is fine).
    """
    order = ORDERS.get(order_id.lstrip("#").strip())
    if order is None:
        return f"No order found with ID {order_id}."
    return f"Order {order_id}: {order['item']} - {order['status']}. {order['detail']}"


@tool
def check_stock(product_name: str) -> str:
    """Check how many units of a product are in stock.

    Args:
        product_name: The product's name, for example "wool hiking socks".
    """
    count = STOCK.get(product_name.lower().strip())
    if count is None:
        return f"We don't sell a product called '{product_name}'."
    return f"{count} in stock." if count else "Out of stock."


def banner(title: str) -> None:
    print(f"\n=== {title} ===")


def main() -> None:
    tools = [get_order_status, check_stock]
    tools_by_name = {t.name: t for t in tools}

    # ---- 1. What the model will see about each tool -----------------------
    banner("1. What the model sees")
    for t in tools:
        print(f"{t.name}: {t.description.splitlines()[0]}")
        print("   arguments:", t.args)

    # ---- 2. A tool is just a function: no AI involved ---------------------
    banner("2. Calling a tool directly (no model yet)")
    print(get_order_status.invoke({"order_id": "1042"}))
    print(get_order_status.invoke({"order_id": "9999"}))  # errors can be plain text

    # ---- 3. Tell the model about the tools, then ask ----------------------
    model_with_tools = get_model().bind_tools(tools)
    messages = [SystemMessage(TOOLS_SYSTEM_PROMPT), HumanMessage(CUSTOMER_MESSAGE)]
    ai_msg = model_with_tools.invoke(messages)

    banner("3. The model's tool call (a REQUEST, nothing has run yet)")
    if not ai_msg.tool_calls:
        print("The model answered without a tool this time:\n", ai_msg.text)
        return
    for call in ai_msg.tool_calls:
        print(f"name={call['name']}  args={call['args']}  id={call['id']}")

    # ---- 4. YOU run the tools and send the results back -------------------
    messages.append(ai_msg)  # keep the model's request in the history
    banner("4. Running the tools ourselves")
    for call in ai_msg.tool_calls:
        result = tools_by_name[call["name"]].invoke(call)  # returns a ToolMessage
        messages.append(result)
        print(type(result).__name__, "->", result.content)

    # ---- 5. The model turns the tool result into a friendly answer --------
    final = model_with_tools.invoke(messages)
    banner("5. ShopDesk's final answer")
    print(final.text)

    # ---- 6. No tool needed? The model can just answer ---------------------
    banner("6. A message that needs no tool")
    reply = model_with_tools.invoke(
        [SystemMessage(TOOLS_SYSTEM_PROMPT), HumanMessage(THANKS_MESSAGE)]
    )
    print("tool calls:", reply.tool_calls)  # usually an empty list
    print(reply.text)

    print(
        "\nNotice: we wrote the 'ask, run, answer' loop by hand. "
        "Day 10 builds this same loop as a LangGraph graph."
    )


if __name__ == "__main__":
    main()
