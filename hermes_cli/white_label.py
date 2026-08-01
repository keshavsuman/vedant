"""White-label control plane: load ``white_label.yaml`` and apply it.

Source of truth for product branding, tone/soul, and capability defaults.
Runtime precedence:

1. ``$HERMES_HOME/white_label.yaml`` (or KESHAV_HOME / TOMORROW_HOME)
2. ``<repo>/white_label.yaml``
3. Hardcoded fallbacks in callers (``brand.py``, ``default_soul.py``, …)

Use ``tomorrow customize`` to inspect and apply settings into the live
data home (SOUL.md + config.yaml).
"""

from __future__ import annotations

import copy
import os
import shutil
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[1]
_CACHE: dict[str, Any] | None = None

_FALLBACK_BRAND: dict[str, Any] = {
    "product_name": "Tomorrow",
    "product_name_full": "Tomorrow",
    "product_tagline": (
        "Virtual Executive for Decision-making, Automation, Navigation, and Tasks"
    ),
    "org_name": "Keshav",
    "cli_name": "tomorrow",
    "default_skin": "keshav",
    "home_dirname": ".keshav",
    "home_dirname_win": "keshav",
    "home_env_vars": ["KESHAV_HOME", "TOMORROW_HOME", "HERMES_HOME"],
}


def _deep_merge(base: dict, overlay: dict) -> dict:
    """Recursively merge *overlay* into a copy of *base* (dicts only)."""
    out = copy.deepcopy(base)
    for key, value in (overlay or {}).items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = copy.deepcopy(value)
    return out


def _home_white_label_path() -> Path | None:
    for key in ("KESHAV_HOME", "TOMORROW_HOME", "HERMES_HOME"):
        raw = os.environ.get(key)
        if raw:
            return Path(raw).expanduser() / "white_label.yaml"
    try:
        from hermes_constants import get_hermes_home

        return get_hermes_home() / "white_label.yaml"
    except Exception:
        return None


def repo_white_label_path() -> Path:
    return _REPO_ROOT / "white_label.yaml"


def resolve_white_label_paths() -> list[Path]:
    """Paths in load order (base → overlay). Missing files are skipped."""
    paths = [repo_white_label_path()]
    home = _home_white_label_path()
    if home is not None and home.resolve() != paths[0].resolve():
        paths.append(home)
    return paths


def _yaml_load(text: str) -> Any:
    """Load YAML via PyYAML or ruamel.yaml (both are project deps)."""
    try:
        import yaml

        return yaml.safe_load(text)
    except ImportError:
        pass
    try:
        from ruamel.yaml import YAML

        return YAML(typ="safe").load(text)
    except ImportError as exc:
        raise ImportError(
            "PyYAML (or ruamel.yaml) is required to read white_label.yaml. "
            "Install the project venv: pip install -e ."
        ) from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        data = _yaml_load(path.read_text(encoding="utf-8")) or {}
    except ImportError:
        raise
    except (OSError, UnicodeDecodeError, Exception):
        return {}
    return data if isinstance(data, dict) else {}


def load_white_label(*, force: bool = False) -> dict[str, Any]:
    """Load and merge white-label YAML files. Result is cached per process."""
    global _CACHE
    if _CACHE is not None and not force:
        return _CACHE
    merged: dict[str, Any] = {}
    try:
        for path in resolve_white_label_paths():
            merged = _deep_merge(merged, _read_yaml(path))
    except ImportError:
        # Brand/soul callers have hardcoded fallbacks; customize CLI surfaces this.
        merged = {}
    _CACHE = merged
    return merged


def clear_white_label_cache() -> None:
    global _CACHE
    _CACHE = None


def get_brand_section() -> dict[str, Any]:
    brand = load_white_label().get("brand") or {}
    if not isinstance(brand, dict):
        brand = {}
    return {**_FALLBACK_BRAND, **brand}


def get_tone_section() -> dict[str, Any]:
    tone = load_white_label().get("tone") or {}
    return tone if isinstance(tone, dict) else {}


def get_soul_text() -> str:
    text = (get_tone_section().get("soul") or "").strip()
    return text


def get_identity_text() -> str:
    tone = get_tone_section()
    text = (tone.get("identity") or tone.get("soul") or "").strip()
    return text


def get_help_guidance_text() -> str:
    return (get_tone_section().get("help_guidance") or "").strip()


def get_capabilities_config() -> dict[str, Any]:
    caps = load_white_label().get("capabilities") or {}
    if not isinstance(caps, dict):
        return {}
    cfg = caps.get("config") or {}
    return cfg if isinstance(cfg, dict) else {}


def get_tools_platform_toolsets() -> dict[str, Any]:
    tools = load_white_label().get("tools") or {}
    if not isinstance(tools, dict):
        return {}
    pts = tools.get("platform_toolsets") or {}
    return pts if isinstance(pts, dict) else {}


# ---------------------------------------------------------------------------
# customize CLI
# ---------------------------------------------------------------------------


def _cli_name() -> str:
    try:
        from hermes_cli.brand import CLI_NAME

        return CLI_NAME
    except Exception:
        return str(get_brand_section().get("cli_name") or "tomorrow")


def _print_show() -> None:
    data = load_white_label(force=True)
    brand = get_brand_section()
    tone = get_tone_section()
    caps = get_capabilities_config()
    tools = get_tools_platform_toolsets()
    paths = resolve_white_label_paths()

    print(f"{brand.get('product_name')} white-label")
    print()
    print("Sources (later overrides earlier):")
    for p in paths:
        mark = "✓" if p.is_file() else "·"
        print(f"  {mark} {p}")
    print()
    print("Brand:")
    for key in (
        "product_name",
        "org_name",
        "cli_name",
        "default_skin",
        "home_dirname",
        "product_tagline",
    ):
        print(f"  {key}: {brand.get(key)}")
    print()
    soul = (tone.get("soul") or "").strip()
    print("Tone / soul:")
    if soul:
        preview = soul.replace("\n", " ")
        if len(preview) > 160:
            preview = preview[:157] + "..."
        print(f"  {preview}")
    else:
        print("  (not set — using code fallbacks)")
    print()
    print("Capabilities → config.yaml keys:")
    if caps:
        for section, value in caps.items():
            print(f"  {section}: {value}")
    else:
        print("  (none)")
    print()
    print("Tools platform_toolsets:")
    if tools:
        for platform, sets in tools.items():
            print(f"  {platform}: {sets}")
    else:
        print(f"  (none — use `{_cli_name()} tools` to toggle interactively)")
    print()
    mem = (caps.get("memory") or {}) if isinstance(caps.get("memory"), dict) else {}
    print("Memory:")
    print(f"  memory_enabled: {mem.get('memory_enabled', '(inherit)')}")
    print(f"  provider: {mem.get('provider', '(inherit / empty = built-in)')}")
    # Silence unused warning when data only used for force reload side effect
    _ = data


def _open_editor(path: Path) -> int:
    editor = os.environ.get("EDITOR") or os.environ.get("VISUAL") or "nano"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file():
        src = repo_white_label_path()
        if src.is_file():
            shutil.copy2(src, path)
        else:
            path.write_text(
                "# white_label.yaml — see repo white_label.yaml for schema\n",
                encoding="utf-8",
            )
    print(f"Opening {path} in {editor}…")
    return os.spawnvp(os.P_WAIT, editor, [editor, str(path)])


def apply_white_label(
    *,
    force_soul: bool = False,
    dry_run: bool = False,
) -> list[str]:
    """Apply white-label settings into the live data home.

    Returns a list of human-readable action lines.
    """
    from hermes_constants import get_hermes_home
    from hermes_cli.default_soul import is_legacy_template_soul

    clear_white_label_cache()
    brand = get_brand_section()
    soul_text = get_soul_text()
    caps = get_capabilities_config()
    tools = get_tools_platform_toolsets()
    home = get_hermes_home()
    actions: list[str] = []

    # 1) Persist effective white_label.yaml into the data home
    repo_src = repo_white_label_path()
    dest_wl = home / "white_label.yaml"
    if repo_src.is_file() and not dest_wl.is_file():
        actions.append(f"copy white_label.yaml → {dest_wl}")
        if not dry_run:
            home.mkdir(parents=True, exist_ok=True)
            shutil.copy2(repo_src, dest_wl)
    elif dest_wl.is_file():
        actions.append(f"keep existing {dest_wl} (edit with `{_cli_name()} customize edit`)")
    elif repo_src.is_file():
        actions.append(f"would copy white_label.yaml → {dest_wl}")

    # 2) SOUL.md
    if soul_text:
        soul_path = home / "SOUL.md"
        write_soul = False
        if not soul_path.exists():
            write_soul = True
            reason = "create"
        else:
            try:
                existing = soul_path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                existing = ""
            if force_soul:
                write_soul = True
                reason = "overwrite (--force-soul)"
            elif is_legacy_template_soul(existing):
                write_soul = True
                reason = "upgrade legacy template"
            elif existing.strip() == soul_text.strip():
                reason = "already matches"
            else:
                reason = "skip customized SOUL.md (use --force-soul to overwrite)"
        if write_soul:
            actions.append(f"SOUL.md ← tone.soul ({reason})")
            if not dry_run:
                home.mkdir(parents=True, exist_ok=True)
                soul_path.write_text(soul_text.rstrip() + "\n", encoding="utf-8")
        else:
            actions.append(f"SOUL.md: {reason}")

    # 3) config.yaml merge (capabilities, tools, default skin)
    skin = brand.get("default_skin")
    if caps or tools or skin:
        from hermes_cli.config import load_config, save_config

        cfg = load_config()
        dirty = False
        if caps:
            actions.append(f"merge capabilities.config into {home / 'config.yaml'}")
            if not dry_run:
                cfg = _deep_merge(cfg, caps)
                dirty = True
        if tools:
            actions.append("merge tools.platform_toolsets into config.yaml")
            if not dry_run:
                existing_pts = cfg.get("platform_toolsets")
                if not isinstance(existing_pts, dict):
                    existing_pts = {}
                cfg["platform_toolsets"] = _deep_merge(existing_pts, tools)
                dirty = True
        if skin:
            display = cfg.setdefault("display", {})
            if isinstance(display, dict) and display.get("skin") != skin:
                actions.append(f"display.skin → {skin}")
                if not dry_run:
                    display["skin"] = skin
                    dirty = True
        if dirty and not dry_run:
            save_config(cfg)

    if dry_run:
        actions.insert(0, "[dry-run] no files written")
    return actions


def customize_command(args) -> None:
    """Entry point for ``tomorrow customize``."""
    sub = getattr(args, "customize_command", None) or "show"
    try:
        # Force a real YAML load so missing deps fail loudly here, not silently.
        clear_white_label_cache()
        for path in resolve_white_label_paths():
            if path.is_file():
                _read_yaml(path)
                break
        else:
            # Still allow show/path when no file exists yet
            pass
    except ImportError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if sub == "show":
        _print_show()
        return
    if sub == "path":
        for p in resolve_white_label_paths():
            print(p)
        return
    if sub == "edit":
        home_path = _home_white_label_path()
        if home_path is None:
            print("Could not resolve data home for white_label.yaml", file=sys.stderr)
            sys.exit(1)
        code = _open_editor(home_path)
        clear_white_label_cache()
        print()
        print(f"Apply with:  {_cli_name()} customize apply")
        sys.exit(code if isinstance(code, int) else 0)
    if sub == "apply":
        actions = apply_white_label(
            force_soul=bool(getattr(args, "force_soul", False)),
            dry_run=bool(getattr(args, "dry_run", False)),
        )
        for line in actions:
            print(f"  • {line}")
        print()
        print("Done. New sessions pick up SOUL/config changes immediately.")
        print(
            f"Tip: interactive tools → `{_cli_name()} tools`  |  "
            f"skin → `{_cli_name()} skin use <name>`"
        )
        return
    print(f"Unknown customize command: {sub}", file=sys.stderr)
    sys.exit(2)
