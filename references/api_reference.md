# TmuxController API Reference

## Scripts

All scripts are in `scripts/` and use PEP 723 inline metadata (`requires-python = ">=3.10"`). Run them with `uv run`.

### `list_sessions.py`

List available tmux sessions. Run this first to discover sessions.

```bash
uv run scripts/list_sessions.py
```

### `run_command.py`

Execute a command in a tmux session and get the output.

```bash
uv run scripts/run_command.py <session> "<command>" [--timeout SECONDS] [--no-markers]
```

| Argument | Description |
|----------|-------------|
| `session` | tmux session name |
| `command` | Shell command to execute |
| `--timeout` | Max wait time in seconds (default: 30) |
| `--no-markers` | Use prompt detection instead of UUID markers |

Exit codes: 0=success, 1=tmux error, 2=timeout.

### `read_buffer.py`

Read the current visible content of a tmux pane without executing anything.

```bash
uv run scripts/read_buffer.py <session> [--lines N] [--history]
```

| Argument | Description |
|----------|-------------|
| `session` | tmux session name |
| `--lines` | Return only the last N lines |
| `--history` | Include scroll-back history |

### `send_keys.py`

Send keystrokes to a tmux session without waiting for completion. For interactive programs, streaming commands, or control sequences.

```bash
uv run scripts/send_keys.py <session> "<text>"
uv run scripts/send_keys.py <session> "<text>" --no-enter
uv run scripts/send_keys.py <session> --ctrl C
```

| Argument | Description |
|----------|-------------|
| `session` | tmux session name |
| `text` | Text to send (optional if `--ctrl` is used) |
| `--no-enter` | Do not press Enter after text |
| `--ctrl` | Send Ctrl+KEY (e.g. `C`, `Z`, `[` for Escape) |

## TmuxController Class (for advanced usage)

```python
from tmux_bridge import TmuxController

ctrl = TmuxController("session_name", default_timeout=30.0)
```

### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `session_name` | `str` | required | tmux session name or `session:window.pane` target |
| `prompt_pattern` | `str` | `r"[\$#>] $"` | Regex for prompt detection fallback |
| `default_timeout` | `float` | `30.0` | Default timeout in seconds |
| `poll_interval` | `float` | `0.3` | Seconds between buffer polls |

### Methods

- `send_keys(text, *, enter=True)` — Send keystrokes to the pane
- `read_buffer(lines=None, *, history=False)` — Read pane content (ANSI stripped)
- `execute_and_wait(command, *, timeout=None, poll_interval=None, use_markers=True)` — Run command and return output
- `list_sessions()` — (static) List all tmux session names
- `session_exists(name)` — (static) Check if a session exists

### Exceptions

- `TmuxError` — Base exception
- `SessionNotFoundError` — Target session does not exist
- `CommandTimeoutError` — Command exceeded timeout
