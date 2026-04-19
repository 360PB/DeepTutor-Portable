"""Pure-ANSI terminal UI toolkit — zero external dependencies.

Provides banner, inline arrow-key selector, confirm, text input, step
headers, coloured log helpers, spinner, and countdown.  Designed for a
minimal / industrial aesthetic inspired by Claude Code.
"""
from __future__ import annotations

import getpass
import os
import shutil
import sys
import textwrap
import time
from contextlib import contextmanager
from typing import Generator

# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------

def _is_color() -> bool:
    return sys.stdout.isatty() and os.environ.get("TERM", "dumb") != "dumb"


def _wrap(text: str, code: str) -> str:
    if not _is_color():
        return text
    return f"\033[{code}m{text}\033[0m"


def accent(text: str) -> str:
    return _wrap(text, "38;5;111")


def success(text: str) -> str:
    return _wrap(text, "38;5;78")


def warn(text: str) -> str:
    return _wrap(text, "38;5;214")


def error(text: str) -> str:
    return _wrap(text, "38;5;203")


def dim(text: str) -> str:
    return _wrap(text, "2")


def bold(text: str) -> str:
    return _wrap(text, "1")


# ---------------------------------------------------------------------------
# Terminal geometry
# ---------------------------------------------------------------------------

def term_width() -> int:
    return min(max(shutil.get_terminal_size((80, 24)).columns, 60), 100)


# ---------------------------------------------------------------------------
# Low-level key reading (Unix / Windows)
# ---------------------------------------------------------------------------

def _read_key() -> str:
    """Read a single keypress.  Returns 'up', 'down', 'enter', or char."""
    try:
        import tty
        import termios

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                seq = sys.stdin.read(2)
                if seq == "[A":
                    return "up"
                if seq == "[B":
                    return "down"
                return "esc"
            if ch in ("\r", "\n"):
                return "enter"
            if ch == "\x03":
                raise KeyboardInterrupt
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    except ImportError:
        # Windows fallback
        import msvcrt  # type: ignore[import-untyped]

        ch = msvcrt.getwch()
        if ch == "\xe0":
            code = msvcrt.getwch()
            if code == "H":
                return "up"
            if code == "P":
                return "down"
            return "esc"
        if ch in ("\r", "\n"):
            return "enter"
        if ch == "\x03":
            raise KeyboardInterrupt
        return ch


# ---------------------------------------------------------------------------
# Banner
# ---------------------------------------------------------------------------

def banner(title: str, lines: list[str] | None = None) -> None:
    w = term_width()
    inner = w - 4  # usable chars between "│ " and " │"

    print()
    dashes = max(w - 4 - len(title), 0)
    print(f"┌ {accent(title)} " + "─" * dashes + "┐")

    if lines:
        print(f"│{' ' * (w - 2)}│")
        for line in lines:
            for wrapped in textwrap.wrap(line, width=inner) or [""]:
                print(f"│ {dim(wrapped.ljust(inner))} │")
        print(f"│{' ' * (w - 2)}│")

    print("└" + "─" * (w - 2) + "┘")
    print()


# ---------------------------------------------------------------------------
# Inline arrow-key selector
# ---------------------------------------------------------------------------

def select(prompt: str, options: list[tuple[str, str, str]]) -> str:
    """Arrow-key selector.  *options* is a list of ``(value, label, desc)``.

    Returns the *value* of the chosen option.  Falls back to numbered
    input when stdin is not a tty.
    """
    if not sys.stdin.isatty():
        return _select_fallback(prompt, options)

    idx = 0
    total = len(options)

    print(dim(f"  {prompt}"))
    print()

    def _render() -> None:
        for i, (_, label, desc) in enumerate(options):
            if i == idx:
                marker = accent("> ")
                text = f"{bold(label)}  {dim(desc)}" if desc else bold(label)
            else:
                marker = "  "
                text = dim(f"{label}  {desc}") if desc else dim(label)
            print(f"  {marker}{text}")

    _render()

    while True:
        key = _read_key()
        if key == "up":
            idx = (idx - 1) % total
        elif key == "down":
            idx = (idx + 1) % total
        elif key == "enter":
            # Move past the option block
            sys.stdout.write(f"\033[{total}A")
            sys.stdout.write(f"\033[J")
            chosen_label = options[idx][1]
            chosen_desc = options[idx][2]
            print(f"  {accent('>')} {bold(chosen_label)}  {dim(chosen_desc)}")
            print()
            return options[idx][0]
        elif key == "esc":
            continue
        else:
            continue

        # Redraw: move cursor up by `total` lines, clear, re-render
        sys.stdout.write(f"\033[{total}A")
        sys.stdout.write(f"\033[J")
        _render()


def _select_fallback(prompt: str, options: list[tuple[str, str, str]]) -> str:
    print(f"  {prompt}")
    for i, (_, label, desc) in enumerate(options, 1):
        print(f"  {i}. {label}  {desc}")
    while True:
        answer = input("  > ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return options[int(answer) - 1][0]
        for value, label, _ in options:
            if answer in (value, label):
                return value
        print(warn("  Please choose a valid option."))


# ---------------------------------------------------------------------------
# Confirm (Y/n)
# ---------------------------------------------------------------------------

def confirm(prompt: str, default: bool = True) -> bool:
    hint = "[Y/n]" if default else "[y/N]"
    while True:
        answer = input(f"  {prompt} {dim(hint)} ").strip().lower()
        if not answer:
            return default
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print(warn("  Please answer y or n."))


# ---------------------------------------------------------------------------
# Text input
# ---------------------------------------------------------------------------

def text_input(prompt: str, default: str = "", secret: bool = False) -> str:
    display = f"  {prompt}"
    if default and not secret:
        display += f" {dim(f'[{default}]')}"
    display += dim(": ")

    if secret:
        value = getpass.getpass(display)
    else:
        value = input(display).strip()
    return value or default


# ---------------------------------------------------------------------------
# Step header
# ---------------------------------------------------------------------------

def step(current: int, total: int | str, title: str) -> None:
    print()
    w = term_width()
    label = f" {current}/{total} "
    left = (w - len(label)) // 2
    right = w - left - len(label)
    print(dim("─" * left + label + "─" * right))
    print(f"  {bold(title)}")
    print()


# ---------------------------------------------------------------------------
# Log helpers
# ---------------------------------------------------------------------------

def log_info(msg: str) -> None:
    print(f"  {accent('·')} {msg}")


def log_success(msg: str) -> None:
    print(f"  {success('✓')} {msg}")


def log_warn(msg: str) -> None:
    print(f"  {warn('!')} {msg}")


def log_error(msg: str) -> None:
    print(f"  {error('✗')} {msg}")


# ---------------------------------------------------------------------------
# Spinner (context manager)
# ---------------------------------------------------------------------------

_SPINNER_FRAMES = ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")


@contextmanager
def spinner(label: str) -> Generator[None, None, None]:
    """Simple braille-dot spinner shown while the body executes."""
    import threading

    stop = threading.Event()

    def _spin() -> None:
        i = 0
        while not stop.is_set():
            frame = _SPINNER_FRAMES[i % len(_SPINNER_FRAMES)]
            sys.stdout.write(f"\r  {accent(frame)} {label}")
            sys.stdout.flush()
            i += 1
            stop.wait(0.08)
        sys.stdout.write("\r" + " " * (len(label) + 6) + "\r")
        sys.stdout.flush()

    t = threading.Thread(target=_spin, daemon=True)
    t.start()
    try:
        yield
    finally:
        stop.set()
        t.join()


# ---------------------------------------------------------------------------
# Countdown
# ---------------------------------------------------------------------------

def countdown(seconds: int, label: str = "Starting in") -> None:
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\r  {dim(label)} {accent(str(remaining))}s ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " " * (len(label) + 12) + "\r")
    sys.stdout.flush()
