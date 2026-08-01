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
