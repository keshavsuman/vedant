"""Product branding constants for the Vedant / Localstreet white-label.

User-facing surfaces (CLI, TUI, gateway messages, system prompt, logs that
print to the terminal) should import from here instead of hardcoding
legacy product names.
"""

PRODUCT_NAME = "Vedant"
PRODUCT_NAME_FULL = "Vedant"
PRODUCT_TAGLINE = (
    "Virtual Executive for Decision-making, Automation, Navigation, and Tasks"
)
ORG_NAME = "Localstreet"
CLI_NAME = "vedant"
DEFAULT_SKIN = "localstreet"
HOME_DIRNAME = ".localstreet"
HOME_DIRNAME_WIN = "localstreet"

# Env vars checked (in order) for the data home directory.
HOME_ENV_VARS = ("LOCALSTREET_HOME", "VEDANT_HOME", "HERMES_HOME")


def user_facing_text(value: str) -> str:
    """Replace legacy product identifiers in text intended for end users.

    Internal module, protocol, and compatibility names deliberately remain
    unchanged. Call this only at presentation boundaries such as CLI help.
    """
    return (
        value.replace("~/.hermes", f"~/{HOME_DIRNAME}")
        .replace("HERMES_", "VEDANT_")
        .replace("Hermes", PRODUCT_NAME)
        .replace("hermes", CLI_NAME)
    )
