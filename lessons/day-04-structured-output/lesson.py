"""Day 04 - Structured output: get an object back, not a paragraph.

ShopDesk scenario
-----------------
ShopDesk's inbox is full of messy human messages. Before anyone (or any tool)
can act on them, each one must become a tidy TICKET: a category, an urgency,
an order number, a one-line summary. Today the model fills in that ticket.

What you will learn
-------------------
1. Why "please reply in JSON" is fragile
2. A schema    - a Pydantic class that describes the ticket you want
3. with_structured_output - the model returns a Ticket object, not text
4. Using it    - normal Python: if/else on fields, model_dump() to a dict
5. include_raw - keep the original AIMessage next to the parsed Ticket
6. Validation  - Pydantic rejects data that breaks the schema

Run it (from the repo root, after setting up .env - see the README)
-------------------------------------------------------------------
    uv run python lessons/day-04-structured-output/lesson.py
"""

import json
from typing import Literal

from langchain.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field, ValidationError

from shared.config import get_model
from shared.shopdesk import INBOX_MESSAGES, TRIAGE_SYSTEM_PROMPT


# ---- The schema: the shape you want back ------------------------------------
# The class docstring, the field names, the types and the descriptions are all
# sent to the model. Like a tool docstring (Day 3), they are a prompt.
class Ticket(BaseModel):
    """A support ticket created from one customer message."""

    category: Literal[
        "order_status", "refund", "product_question", "complaint", "other"
    ] = Field(description="What the customer mainly wants.")
    urgency: Literal["low", "medium", "high"] = Field(
        description="high = deadline or very upset customer; low = no rush."
    )
    order_id: str | None = Field(
        description="The order number without '#', or null if none is mentioned."
    )
    summary: str = Field(description="One short sentence describing the problem.")
    needs_human: bool = Field(
        description="True if the customer asks for a person or a manager."
    )


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def main() -> None:
    model = get_model()
    urgent, relaxed = INBOX_MESSAGES

    # 1. The fragile way: ask nicely for JSON and hope --------------------------
    section("1. Asking for JSON in plain text")
    reply = model.invoke(
        [
            SystemMessage(TRIAGE_SYSTEM_PROMPT),
            HumanMessage(
                f"{urgent}\n\nReturn the ticket as JSON with keys: "
                "category, urgency, order_id, summary, needs_human."
            ),
        ]
    )
    print("Raw text from the model:\n", reply.text)
    try:
        json.loads(reply.text)
        print("-> json.loads worked this time. It is not guaranteed.")
    except json.JSONDecodeError as err:
        print(f"-> json.loads FAILED ({err.msg}). Extra words or code fences break it.")

    # 2. The reliable way: bind the schema to the model -------------------------
    section("2. with_structured_output(Ticket)")
    triage_model = model.with_structured_output(Ticket)
    ticket = triage_model.invoke(
        [SystemMessage(TRIAGE_SYSTEM_PROMPT), HumanMessage(urgent)]
    )
    print("type:", type(ticket).__name__)  # a Ticket, not an AIMessage
    print("category:", ticket.category)
    print("urgency:", ticket.urgency)
    print("order_id:", ticket.order_id)
    print("needs_human:", ticket.needs_human)
    print("summary:", ticket.summary)

    # 3. Use it like any Python object ------------------------------------------
    section("3. Route both messages with plain if/else")
    for text in (urgent, relaxed):
        t = triage_model.invoke(
            [SystemMessage(TRIAGE_SYSTEM_PROMPT), HumanMessage(text)]
        )
        if t.needs_human or t.urgency == "high":
            queue = "ESCALATE to a human"
        elif t.category == "product_question":
            queue = "auto-reply from the product catalog"
        else:
            queue = "normal queue"
        print(f"- [{t.urgency:>6}] {t.category:<16} -> {queue}")
    print("As a plain dict (ready for JSON or a database):", ticket.model_dump())

    # 4. Keep the raw AIMessage too ---------------------------------------------
    section("4. include_raw=True")
    raw_model = model.with_structured_output(Ticket, include_raw=True)
    result = raw_model.invoke(
        [SystemMessage(TRIAGE_SYSTEM_PROMPT), HumanMessage(relaxed)]
    )
    print("keys:", list(result.keys()))
    print("raw is a:", type(result["raw"]).__name__)
    print("parsed is a:", type(result["parsed"]).__name__)
    print("parsing_error:", result["parsing_error"])
    print("tokens used:", result["raw"].usage_metadata)

    # 5. The schema is enforced by Pydantic -------------------------------------
    section("5. Bad data is rejected")
    try:
        Ticket(
            category="banana",
            urgency="high",
            order_id=None,
            summary="x",
            needs_human=False,
        )
    except ValidationError as err:
        first = err.errors()[0]
        print(f"ValidationError on '{first['loc'][0]}': {first['msg']}")

    print(
        "\nDay 7 puts this ticket inside a LangGraph state, so every node can read it."
    )


if __name__ == "__main__":
    main()
