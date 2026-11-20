"""The LLM application under test: a small customer-support assistant.

It answers questions about "Acme Cloud Storage" using a fixed knowledge base
that is passed to Claude as context.
"""

import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

KNOWLEDGE_BASE = (Path(__file__).parent / "knowledge_base.md").read_text()

SYSTEM_PROMPT = f"""You are the customer-support assistant for Acme Cloud Storage.

Answer only from the knowledge base below. If the answer is not in it, say you
don't know and suggest contacting support@acme.example. Be friendly and concise
(at most 4 sentences). Never invent prices, limits or policies.

<knowledge_base>
{KNOWLEDGE_BASE}
</knowledge_base>"""

_client = anthropic.Anthropic()


def answer(question: str) -> str:
    """Return the assistant's reply to a single customer question."""
    response = _client.messages.create(
        model=os.getenv("APP_MODEL", "claude-opus-5-5"),
        max_tokens=1024,
        output_config={"effort": "low"},
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": question}],
    )
    if response.stop_reason == "refusal":
        return "Sorry, I can't help with that request."
    return "".join(b.text for b in response.content if b.type == "text").strip()


def knowledge_base() -> str:
    return KNOWLEDGE_BASE


if __name__ == "__main__":
    import sys

    print(answer(" ".join(sys.argv[1:]) or "How much does the Pro plan cost?"))
