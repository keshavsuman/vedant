"""Default SOUL.md template seeded into the data home on first run.

Override via ``white_label.yaml`` → ``tone.soul`` (see ``tomorrow customize``).
"""

_FALLBACK_SOUL_MD = (
    "You are Tomorrow, an intelligent AI assistant — Virtual Executive for "
    "Decision-making, Automation, Navigation, and Tasks — by Keshav. "
    "You are helpful, knowledgeable, and direct. You assist users with a wide "
    "range of tasks including answering questions, writing and editing code, "
    "analyzing information, creative work, and executing actions via your tools. "
    "You communicate clearly, admit uncertainty when appropriate, and prioritize "
    "being genuinely useful over being verbose unless otherwise directed below. "
    "Be targeted and efficient in your exploration and investigations."
)


def _resolve_default_soul() -> str:
    try:
        from hermes_cli.white_label import get_soul_text

        text = get_soul_text()
        if text:
            return text
    except Exception:
        pass
    return _FALLBACK_SOUL_MD


DEFAULT_SOUL_MD = _resolve_default_soul()

# Legacy SOUL.md boilerplate that older installers seeded before they were
# switched to write DEFAULT_SOUL_MD. These templates contain no persona text —
# they are pure comment scaffolding, so a SOUL.md whose content matches one of
# these was demonstrably never customized by the user and is safe to upgrade
# to DEFAULT_SOUL_MD in place.
_LEGACY_TEMPLATE_SOULS = (
    (
        "# Hermes Agent Persona\n"
        "\n"
        "<!--\n"
        "This file defines the agent's personality and tone.\n"
        "The agent will embody whatever you write here.\n"
        "Edit this to customize how Hermes communicates with you.\n"
        "\n"
        "Examples:\n"
        '  - "You are a warm, playful assistant who uses kaomoji occasionally."\n'
        '  - "You are a concise technical expert. No fluff, just facts."\n'
        '  - "You speak like a friendly coworker who happens to know everything."\n'
        "\n"
        "This file is loaded fresh each message -- no restart needed.\n"
        "Delete the contents (or this file) to use the default personality.\n"
        "-->"
    ),
    (
        "# Hermes Agent Persona\n"
        "\n"
        "<!--\n"
        "This file defines the agent's personality and tone.\n"
        "The agent will embody whatever you write here.\n"
        "Edit this to customize how Hermes communicates with you.\n"
        "\n"
        "This file is loaded fresh each message -- no restart needed.\n"
        "Delete the contents (or this file) to use the default personality.\n"
        "-->"
    ),
    (
        "# Tomorrow Persona\n"
        "\n"
        "<!--\n"
        "This file defines the agent's personality and tone.\n"
        "The agent will embody whatever you write here.\n"
        "Edit this to customize how Tomorrow communicates with you.\n"
        "\n"
        "This file is loaded fresh each message -- no restart needed.\n"
        "Delete the contents (or this file) to use the default personality.\n"
        "-->"
    ),
)


def _normalize_soul(text: str) -> str:
    """Normalize SOUL.md content for legacy-template comparison."""
    return text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff").strip()


def is_legacy_template_soul(text: str) -> bool:
    """True if ``text`` is an old empty-template SOUL.md (no user persona)."""
    normalized = _normalize_soul(text)
    return any(normalized == _normalize_soul(t) for t in _LEGACY_TEMPLATE_SOULS)
