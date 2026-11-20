"""Day 01 - Chat models: your first call to an LLM.

ShopDesk scenario
-----------------
A customer writes to ShopDesk, an online store's support desk, asking where
their order is. Today ShopDesk does the simplest possible thing: send the
message to a chat model and read the reply.

What you will learn
-------------------
1. init_chat_model - one function that builds a model for ANY provider
2. invoke()        - send a prompt, get an AIMessage back
3. What is inside that AIMessage (text and token usage)
4. temperature     - consistent vs. creative answers
5. max_tokens      - a hard cap on reply length (and cost)

Run it (from the repo root, after setting up .env - see the README)
-------------------------------------------------------------------
    uv run python lessons/day-01-chat-models/lesson.py
"""

from langchain.chat_models import init_chat_model

from shared.config import get_model_name
from shared.shopdesk import CUSTOMER_MESSAGE, SHOP_NAME


def banner(title: str) -> None:
    print(f"\n=== {title} ===")


def main() -> None:
    # MODEL_NAME comes from your .env, e.g. "openai:gpt-4o-mini".
    # The "provider:model" format is what lets one line work for any provider.
    model_name = get_model_name()

    # ---- 1. Build the model ------------------------------------------------
    model = init_chat_model(model_name)

    # ---- 2. Send the customer's message -----------------------------------
    prompt = (
        f"You are {SHOP_NAME}, a friendly support agent for an online store. "
        "Reply to the customer in at most 3 sentences.\n\n"
        f"Customer: {CUSTOMER_MESSAGE}"
    )
    response = model.invoke(prompt)

    banner("2. ShopDesk's reply")
    print(response.text)

    # ---- 3. What actually came back? --------------------------------------
    banner("3. What is inside the response")
    print("type   :", type(response).__name__)  # AIMessage - NOT a plain string!
    print("tokens :", response.usage_metadata)  # input / output / total

    # ---- 4. temperature: consistent vs. creative --------------------------
    # Same prompt, run twice at each setting. Low = steady, high = varied.
    subject_prompt = (
        "Write one short, friendly email subject line replying to this "
        "customer. Output only the subject line.\n\n"
        f"Customer: {CUSTOMER_MESSAGE}"
    )
    banner("4. temperature")
    for temperature in (0, 1):
        try:
            tuned = init_chat_model(model_name, temperature=temperature)
            for run in (1, 2):
                subject = tuned.invoke(subject_prompt).text.strip()
                print(f"temperature={temperature} run {run}: {subject}")
        except Exception as error:  # noqa: BLE001  (providers raise different errors)
            print(f"temperature={temperature} not accepted by this model: {error}")
            break

    # ---- 5. max_tokens: cap the length (and the bill) ---------------------
    banner("5. max_tokens")
    try:
        short = init_chat_model(model_name, max_tokens=30)
        capped = short.invoke(prompt)
        print(capped.text)
        print("output tokens:", capped.usage_metadata["output_tokens"])
    except Exception as error:  # noqa: BLE001  (providers raise different errors)
        print(f"max_tokens not accepted by this model: {error}")

    print(
        "\nNotice: ShopDesk cannot really know where order #1042 is - it has no "
        "way to look it up. Tools (Day 3) fix that."
    )


if __name__ == "__main__":
    main()
