SYSTEM_PROMPT = """You are a helpful enterprise assistant running locally.
Rules:
- If you do not know, say "I don't know".
- If CONTEXT is provided, answer ONLY using that context.
- Be concise, accurate, and practical.
"""


def build_prompt(user_message: str, context: str | None) -> str:
    if context:
        return f"""{SYSTEM_PROMPT}

CONTEXT:
{context}

USER QUESTION:
{user_message}

Answer using only CONTEXT. If the answer is not in CONTEXT, say "I don't know".
"""
    return f"""{SYSTEM_PROMPT}

USER QUESTION:
{user_message}
"""
