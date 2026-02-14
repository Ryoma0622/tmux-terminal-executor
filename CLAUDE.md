# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

tmux-for-agent is a Python bridge (`tmux_bridge.py`) that lets AI agents send commands to and read output from tmux sessions where a human has already authenticated (SSH, Kerberos, etc.). No external dependencies — standard library only, Python 3.10+.

## Commands

**Run tests:**
```bash
uv run -m pytest tests/
```

**Run example (requires a running `tmux new -s myserver` session):**
```bash
uv run example_agent.py
```

## Architecture

This is a single-module library with one main class:

- **`tmux_bridge.py`** — Contains `TmuxController` (a `@dataclass`), exception classes (`TmuxError`, `SessionNotFoundError`, `CommandTimeoutError`), and the `strip_ansi` helper. All tmux interaction goes through `_run_tmux()` which shells out to the `tmux` CLI via `subprocess.run`.

- **Command execution** uses UUID-based echo markers (`__TMUX_BRIDGE_START_<uid>__` / `__TMUX_BRIDGE_END_<uid>__`) to reliably detect completion and extract output. A prompt-pattern fallback exists when `use_markers=False`.

- **Tests** (`tests/test_tmux_bridge.py`) mock `subprocess.run` so no real tmux server is needed. Uses `unittest` (not pytest fixtures). Both scripts include PEP 723 inline metadata for `uv run` support.
