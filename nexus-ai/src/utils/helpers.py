from datetime import datetime, timezone


def make_title(text: str, limit: int = 42) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def build_context(messages: list[dict], system_prompt: str, limit: int = 30) -> list[dict]:
    """System prompt + the most recent `limit` messages, in API format."""
    context = [{"role": "system", "content": system_prompt}] if system_prompt else []
    context += [{"role": m["role"], "content": m["content"]} for m in messages[-limit:]]
    return context


def time_ago(iso: str) -> str:
    try:
        delta = datetime.now(timezone.utc) - datetime.fromisoformat(iso)
    except ValueError:
        return ""
    s = int(delta.total_seconds())
    if s < 60:
        return "just now"
    if s < 3600:
        return f"{s // 60}m ago"
    if s < 86400:
        return f"{s // 3600}h ago"
    return f"{s // 86400}d ago"
