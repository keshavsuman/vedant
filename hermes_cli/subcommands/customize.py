"""``tomorrow customize`` — white-label branding / soul / capability control."""

from __future__ import annotations

from typing import Callable

from hermes_cli.brand import CLI_NAME, PRODUCT_NAME


def build_customize_parser(subparsers, *, cmd_customize: Callable) -> None:
    """Attach the ``customize`` subcommand to ``subparsers``."""
    parser = subparsers.add_parser(
        "customize",
        help="Change branding, tone/soul, memory, and capability defaults",
        description=(
            f"White-label control for {PRODUCT_NAME}. Edit white_label.yaml "
            f"(repo or data home), then apply into SOUL.md and config.yaml. "
            f"Interactive tool toggles: `{CLI_NAME} tools`."
        ),
    )
    sub = parser.add_subparsers(dest="customize_command")

    sub.add_parser("show", help="Show effective white-label settings")
    sub.add_parser("path", help="Print white_label.yaml search paths")
    sub.add_parser(
        "edit",
        help="Edit data-home white_label.yaml in $EDITOR",
    )
    apply_p = sub.add_parser(
        "apply",
        help="Apply white_label.yaml into SOUL.md and config.yaml",
    )
    apply_p.add_argument(
        "--force-soul",
        action="store_true",
        help="Overwrite SOUL.md even if it was customized",
    )
    apply_p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without writing files",
    )

    parser.set_defaults(func=cmd_customize, customize_command="show")
