"""Day 02 - Messages: how a conversation is represented.

ShopDesk scenario
-----------------
On Day 1, ShopDesk promised to "check your order" - something it cannot do.
We stuffed the instructions and the customer's words into one string. Today we
fix both problems using MESSAGES, then handle a follow-up question.

What you will learn
-------------------
1. The three roles: SystemMessage, HumanMessage, AIMessage
2. Passing a LIST of messages to the model (instructions + customer, kept apart)
3. The reply is a message too (an AIMessage)
4. Models have NO memory: each call only knows what you send it
5. Conversation history = a list you keep growing and resend
6. Plain dicts work as messages too

Run it (from the repo root, after setting up .env - see the README)
-------------------------------------------------------------------
    uv run python lessons/day-02-messages/lesson.py
"""

from langchain.messages import AIMessage, HumanMessage, SystemMessage

from shared.config import get_model
from shared.shopdesk import CUSTOMER_MESSAGE, FOLLOW_UP_MESSAGE, SYSTEM_PROMPT


def banner(title: str) -> None:
    print(f"\n=== {title} ===")


def show(messages: list) -> None:
    """Print a conversation one line per message: role | start of the text."""
    for message in messages:
        text = message.text.replace("\n", " ")
        print(f"  {message.type:<6}| {text[:70]}")


def main() -> None:
    model = get_model()  # reads MODEL_NAME from .env (the helper from Day 1)

    # ---- 1. Instructions and customer words, kept apart -------------------
    # SystemMessage = standing rules.  HumanMessage = what the customer said.
    messages = [
        SystemMessage(SYSTEM_PROMPT),
        HumanMessage(CUSTOMER_MESSAGE),
    ]
    reply = model.invoke(messages)

    banner("1. ShopDesk's reply (compare with Day 1: no more fake promises)")
    print(reply.text)

    # ---- 2. The reply is a message too ------------------------------------
    banner("2. The reply is an AIMessage")
    print("is an AIMessage:", isinstance(reply, AIMessage), "| role:", reply.type)

    # ---- 3. The model has NO memory ---------------------------------------
    # The customer follows up. We send ONLY the new message. "it" means
    # nothing to the model, because it never saw the first message.
    forgetful = model.invoke(
        [SystemMessage(SYSTEM_PROMPT), HumanMessage(FOLLOW_UP_MESSAGE)]
    )

    banner("3. Follow-up WITHOUT history (the model has no idea what 'it' is)")
    print("customer:", FOLLOW_UP_MESSAGE)
    print("ShopDesk:", forgetful.text)

    # ---- 4. Conversation history = a list you keep growing ----------------
    # Keep the AI's reply, add the new customer message, and send everything.
    messages.append(reply)  # AIMessage goes straight back into the list
    messages.append(HumanMessage(FOLLOW_UP_MESSAGE))
    remembering = model.invoke(messages)

    banner("4. Follow-up WITH history (we resent the whole conversation)")
    show(messages)
    print("ShopDesk:", remembering.text)

    # ---- 5. Plain dicts work too ------------------------------------------
    # {"role": ..., "content": ...} is the same thing in a lighter format.
    as_dicts = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": CUSTOMER_MESSAGE},
    ]
    banner("5. Same first message, written as dicts")
    print(model.invoke(as_dicts).text)

    print(
        "\nNotice: ShopDesk only 'remembered' because WE resent the list. "
        "Real memory (Week 3) is about storing and managing that list for you."
    )


if __name__ == "__main__":
    main()
