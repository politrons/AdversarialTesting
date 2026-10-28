"""Connect Promptfoo to the real Python bot, not a separate implementation."""

from adversarial_testing.library_bot import answer


def call_api(prompt: str, options: dict, context: dict) -> dict:
    guarded = options.get("config", {}).get("guarded", True)
    return {"output": answer(prompt, guarded=guarded)}
