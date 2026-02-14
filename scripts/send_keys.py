#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Send keystrokes to a tmux session without waiting for completion.

Use this for interactive commands (vim, top), long-running processes
(tail -f), or sending control sequences (Ctrl-C to interrupt).

Usage:
    python3 send_keys.py <session> "<text>"
    python3 send_keys.py <session> "<text>" --no-enter
    python3 send_keys.py <session> --ctrl C

Examples:
    python3 send_keys.py myserver "tail -f /var/log/syslog"
    python3 send_keys.py myserver --ctrl C
    python3 send_keys.py myserver "vim config.yaml"
    python3 send_keys.py myserver ":wq" --no-enter
    python3 send_keys.py myserver --ctrl [        # Escape
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tmux_bridge import TmuxController, TmuxError


# tmux send-keys names for control characters
_CTRL_MAP = {c: f"C-{c}" for c in "abcdefghijklmnopqrstuvwxyz"}
_CTRL_MAP["["] = "Escape"


def main() -> None:
    parser = argparse.ArgumentParser(description="Send keys to a tmux session")
    parser.add_argument("session", help="tmux session name")
    parser.add_argument("text", nargs="?", default=None, help="Text to send")
    parser.add_argument("--no-enter", action="store_true", help="Do not press Enter after text")
    parser.add_argument("--ctrl", metavar="KEY", help="Send Ctrl+KEY (e.g. C, Z, [)")
    args = parser.parse_args()

    if args.text is None and args.ctrl is None:
        parser.error("Provide either text or --ctrl KEY")

    try:
        ctrl = TmuxController(args.session)
        if args.ctrl is not None:
            key = args.ctrl.lower()
            tmux_key = _CTRL_MAP.get(key)
            if tmux_key is None:
                print(f"ERROR: Unknown ctrl key: {args.ctrl!r}", file=sys.stderr)
                sys.exit(1)
            ctrl.send_keys(tmux_key, enter=False)
        if args.text is not None:
            ctrl.send_keys(args.text, enter=not args.no_enter)
    except TmuxError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
