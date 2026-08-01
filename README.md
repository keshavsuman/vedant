# Vedant

**VEDANT** — Virtual Executive for Decision-making, Automation, Navigation, and Tasks.

Personal AI agent by **Localstreet**. Runs in the terminal (CLI / TUI), messaging gateways, and scheduled jobs. Config and state live under `~/.localstreet`.

## Quick start (EC2 / Linux)

```bash
pip install -e .
vedant setup
vedant          # interactive CLI (localstreet teal skin)
# or:
localstreet
```

Data directory: `~/.localstreet` (override with `LOCALSTREET_HOME` or `VEDANT_HOME`).

Skin: `localstreet` (teal) is the default. Switch with `/skin localstreet`.

## Common commands

| Command | Purpose |
|---------|---------|
| `vedant` | Interactive chat |
| `vedant --tui` | Terminal UI |
| `vedant setup` | Configure providers / tools |
| `vedant gateway` | Messaging gateway |
| `vedant whatsapp` | Pair WhatsApp |
| `vedant doctor` | Health checks |

## License

MIT
