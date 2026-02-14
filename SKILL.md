---
name: tmux-terminal-executor
description: >
  Execute commands in another terminal via tmux sessions. Use this skill when the agent needs to:
  run commands in a remote server where a human has already authenticated (SSH, Kerberos, etc.),
  read terminal output from another session, interact with a running process in a separate terminal,
  or perform any task that requires operating in a pre-authenticated tmux session.
  Triggers: "run in tmux", "execute in session", "send command to terminal",
  "read terminal output", "check tmux session", operating on remote/authenticated environments.
---

# tmux-terminal-executor

Execute commands in pre-authenticated tmux sessions. The human sets up the session and authenticates; the agent operates within it.

## Prerequisites

- tmux installed and in PATH
- [uv](https://docs.astral.sh/uv/) installed and in PATH (Python 3.10+ is resolved automatically via PEP 723 inline metadata)
- A running tmux session created by the human (e.g., `tmux new -s myserver`)

## Workflow

### 1. Discover available sessions

```bash
uv run {SKILL_DIR}/scripts/list_sessions.py
```

If no sessions exist, ask the human to create one:
```
tmux new -s <session-name>
```

### 2. Execute a command and get output

```bash
uv run {SKILL_DIR}/scripts/run_command.py <session> "<command>" --timeout 30
```

The script uses UUID echo markers to reliably detect command completion and extract output. ANSI escape sequences are automatically stripped.

For long-running commands, increase the timeout:
```bash
uv run {SKILL_DIR}/scripts/run_command.py myserver "make build" --timeout 120
```

### 3. Read current terminal state (without executing)

```bash
uv run {SKILL_DIR}/scripts/read_buffer.py <session>
uv run {SKILL_DIR}/scripts/read_buffer.py <session> --lines 20
uv run {SKILL_DIR}/scripts/read_buffer.py <session> --history
```

Use this to observe what's currently on screen, check prompts, or monitor running processes.

### 4. Send keystrokes (fire-and-forget)

For interactive programs or long-running commands, use `send_keys.py` to send input without waiting:

```bash
# Start a streaming command
uv run {SKILL_DIR}/scripts/send_keys.py <session> "tail -f /var/log/syslog"

# Read what's on screen after a moment
uv run {SKILL_DIR}/scripts/read_buffer.py <session> --lines 30

# Interrupt with Ctrl-C
uv run {SKILL_DIR}/scripts/send_keys.py <session> --ctrl C
```

**Editing files with vim:**
```bash
uv run {SKILL_DIR}/scripts/send_keys.py <session> "vim config.yaml"
# Wait a moment, then read the screen
uv run {SKILL_DIR}/scripts/read_buffer.py <session>
# Navigate / edit (--no-enter to avoid pressing Enter after the keys)
uv run {SKILL_DIR}/scripts/send_keys.py <session> "iHello world" --no-enter
# Press Escape (Ctrl-[)
uv run {SKILL_DIR}/scripts/send_keys.py <session> --ctrl [
# Save and quit
uv run {SKILL_DIR}/scripts/send_keys.py <session> ":wq"
```

**Pattern: send → read → react loop.** For any interactive or streaming workflow, send a keystroke, read the buffer to see the result, then decide the next action.

## Important Notes

- **Never create or destroy tmux sessions** — only the human manages session lifecycle
- **Commands execute in the human's authenticated context** — respect the trust boundary
- **Timeout handling**: If a command times out (exit code 2), read the buffer to check progress rather than re-running
- **Choosing the right tool**: Use `run_command.py` for commands that finish and produce output. Use `send_keys.py` + `read_buffer.py` for streaming commands (`tail -f`, `watch`), interactive programs (`vim`, `top`, `less`), or any situation where you need to send input incrementally
- **Multiple commands**: Chain with `&&` or `;` in a single `run_command.py` call rather than running multiple sequential calls

## API Reference

For the full Python API and advanced usage, see [references/api_reference.md](references/api_reference.md).
