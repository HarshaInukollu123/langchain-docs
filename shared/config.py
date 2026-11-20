"""Load your .env file and build the chat model used by the lessons.

Every lesson starts from the same two things: the MODEL_NAME you chose in
.env (for example ``openai:gpt-4o-mini``) and the API key for that provider.
This file reads them and fails early with a friendly message if something is
missing, so beginners see "add your key" instead of a long stack trace.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Which environment variable holds the key for which provider prefix.
_PROVIDER_KEYS = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "google_genai": "GOOGLE_API_KEY",
}


def get_model_name() -> str:
    """Return MODEL_NAME from .env after checking the matching API key is set."""
    load_dotenv()  # finds the .env in the repo root, whatever folder you run from

    model_name = os.getenv("MODEL_NAME")
    if not model_name:
        raise SystemExit(
            "MODEL_NAME is not set. Copy .env.example to .env and fill it in "
            "(see the README, step 3)."
        )

    provider = model_name.split(":", 1)[0] if ":" in model_name else None
    key_var = _PROVIDER_KEYS.get(provider)
    if key_var:
        key = os.getenv(key_var, "")
        if not key or key.startswith("your-"):
            raise SystemExit(
                f"{key_var} is missing or still the placeholder. Open your .env "
                f"file and paste your own key (MODEL_NAME={model_name})."
            )
    return model_name


def get_model(**kwargs):
    """Build the chat model from .env. Extra kwargs (temperature, ...) pass through."""
    return init_chat_model(get_model_name(), **kwargs)
