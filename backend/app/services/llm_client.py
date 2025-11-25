from ..schemas import ChatRequest


def generate_chat_response(request: ChatRequest) -> str:
    """Return a canned reply; replace with a real LLM client."""
    prefix = f"Plot {request.plot_id}: " if request.plot_id else ""
    return f"{prefix}Thanks for your question. (stub reply) You asked: {request.question}"

