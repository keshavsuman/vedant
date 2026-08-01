# Tomorrow

**TOMORROW** — Virtual Executive for Decision-making, Automation, Navigation, and Tasks.

Personal AI agent by **Keshav**. Runs in the terminal (CLI / TUI), messaging gateways, and scheduled jobs. Config and state live under `~/.keshav`.

## Quick start (EC2 / Linux)

```bash
pip install -e .
tomorrow setup
tomorrow          # interactive CLI (keshav teal skin)
# or:
keshav
```

Data directory: `~/.keshav` (override with `KESHAV_HOME` or `TOMORROW_HOME`).

Skin: `keshav` (teal) is the default. Switch with `/skin keshav`.

## Common commands

| Command | Purpose |
|---------|---------|
| `tomorrow` | Interactive chat |
| `tomorrow --tui` | Terminal UI |
| `tomorrow setup` | Configure providers / tools |
| `tomorrow gateway` | Messaging gateway |
| `tomorrow whatsapp` | Pair WhatsApp |
| `tomorrow doctor` | Health checks |
| `tomorrow customize` | Branding, soul/tone, memory, capability defaults |

White-label control file: `white_label.yaml` — see [WHITE_LABEL.md](WHITE_LABEL.md).

## License

MIT
