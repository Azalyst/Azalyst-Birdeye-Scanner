def format_explain_response(original_response: str, signal_data: dict) -> str:
    """Wrap LLM response with reasoning, confidence, and disclaimer."""
    return f"""
{original_response}

---
**Analysis Confidence:** {signal_data.get('confidence','N/A')}
**Key Factors:** {signal_data.get('reasons',[])}

⚠️ Disclaimer: This is an automated research signal, not financial advice.
Always verify independently and never invest more than you can afford to lose.
"""
