
def format_soap_note(
    subjective: str,
    objective: str,
    assessment: str,
    plan: str,
) -> str:
    """Format SOAP components into a clean text block."""
    return (
        f"SUBJECTIVE\n{subjective}\n\n"
        f"OBJECTIVE\n{objective}\n\n"
        f"ASSESSMENT\n{assessment}\n\n"
        f"PLAN\n{plan}"
    )


def truncate(text: str, max_chars: int = 300, suffix: str = "...") -> str:
    """Truncate long text for display/logging."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + suffix
