"""Product branding constants for the Tomorrow / Keshav white-label.

Values are loaded from ``white_label.yaml`` (repo + data-home overlay) with
hardcoded fallbacks so imports never fail. Edit the YAML and restart the
process (or run ``tomorrow customize apply``) to change branding.

User-facing surfaces (CLI, TUI, gateway messages, system prompt, logs that
print to the terminal) should import from here instead of hardcoding
legacy product names.
"""

from __future__ import annotations

try:
    from hermes_cli.white_label import get_brand_section

    _brand = get_brand_section()
except Exception:
    _brand = {}

PRODUCT_NAME = str(_brand.get("product_name") or "Tomorrow")
PRODUCT_NAME_FULL = str(_brand.get("product_name_full") or PRODUCT_NAME)
PRODUCT_TAGLINE = str(
    _brand.get("product_tagline")
    or "Virtual Executive for Decision-making, Automation, Navigation, and Tasks"
)
ORG_NAME = str(_brand.get("org_name") or "Keshav")
CLI_NAME = str(_brand.get("cli_name") or "tomorrow")
DEFAULT_SKIN = str(_brand.get("default_skin") or "keshav")
HOME_DIRNAME = str(_brand.get("home_dirname") or ".keshav")
HOME_DIRNAME_WIN = str(_brand.get("home_dirname_win") or "keshav")

_env = _brand.get("home_env_vars")
if isinstance(_env, (list, tuple)) and _env:
    HOME_ENV_VARS = tuple(str(x) for x in _env)
else:
    HOME_ENV_VARS = ("KESHAV_HOME", "TOMORROW_HOME", "HERMES_HOME")


def user_facing_text(value: str) -> str:
    """Replace legacy product identifiers in text intended for end users.

    Internal module, protocol, and compatibility names deliberately remain
    unchanged. Call this only at presentation boundaries such as CLI help.
    """
    return (
        value.replace("~/.hermes", f"~/{HOME_DIRNAME}")
        .replace("HERMES_", "TOMORROW_")
        .replace("Hermes", PRODUCT_NAME)
        .replace("hermes", CLI_NAME)
    )
