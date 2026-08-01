# White-label control (Tomorrow / Keshav)

Change branding, tone, memory, and capability defaults without hunting through the codebase.

## Control file

| Location | Role |
|----------|------|
| `white_label.yaml` (repo root) | Ship defaults for your fork |
| `~/.keshav/white_label.yaml` | Live overrides (wins over repo) |

```bash
tomorrow customize show          # effective settings + source paths
tomorrow customize edit          # open data-home YAML in $EDITOR
tomorrow customize apply         # write SOUL.md + merge into config.yaml
tomorrow customize apply --dry-run
tomorrow customize apply --force-soul   # overwrite a customized SOUL.md
tomorrow customize path
```

## What each section controls

### `brand`
Product name, org, CLI name, default skin, home directory label. Loaded into `hermes_cli/brand.py` at process start — restart CLI/gateway after changing names.

### `tone`
- **`soul`** — written to `~/.keshav/SOUL.md` on apply / first install. SOUL is re-read every turn (tone changes without restart).
- **`identity`** — system-prompt fallback when SOUL.md is missing.
- **`help_guidance`** — how the agent describes itself when helping with the product.

You can also edit `~/.keshav/SOUL.md` directly anytime.

### `capabilities.config`
Deep-merged into `~/.keshav/config.yaml` on apply. Use this for:

- `display.skin`
- `memory.memory_enabled` / `memory.provider` / `memory.user_profile_enabled`

Empty `memory.provider` = built-in memory only. Set a provider name (`mem0`, `honcho`, …) after that plugin is installed.

### `tools.platform_toolsets` (optional)
Default toolset lists per platform (`cli`, `telegram`, …). Day-to-day toggles are easier with:

```bash
tomorrow tools
```

## Everyday knobs (outside white_label.yaml)

| Want to change… | Command / file |
|-----------------|----------------|
| Tools per platform | `tomorrow tools` |
| Skin / colors | `tomorrow skin use <name>` or `display.skin` in config |
| Model / provider | `tomorrow model` / `tomorrow setup model` |
| Memory provider | `capabilities.config.memory` then apply, or `tomorrow config set memory.provider …` |
| Personality live | edit `~/.keshav/SOUL.md` |
| Data directory | `export KESHAV_HOME=/path` (or `TOMORROW_HOME`) |

## Rebrand checklist

1. Edit repo `white_label.yaml` (`brand` + `tone`).
2. Optionally add a skin in `hermes_cli/skin_engine.py` and set `brand.default_skin`.
3. Run `tomorrow customize apply --force-soul` on the deploy host.
4. Restart `tomorrow gateway` if it is running (brand constants are process-scoped).
5. Keep internal Python module names (`hermes_cli`, `get_hermes_home`) — only user-facing strings go through branding.
