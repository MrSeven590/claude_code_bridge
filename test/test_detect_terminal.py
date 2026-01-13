from __future__ import annotations

import terminal


def _clear_terminal_env(monkeypatch) -> None:
    monkeypatch.delenv("WEZTERM_PANE", raising=False)
    monkeypatch.delenv("TMUX", raising=False)
    monkeypatch.delenv("TMUX_PANE", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")


def test_detect_terminal_prefers_current_tmux_session(monkeypatch) -> None:
    _clear_terminal_env(monkeypatch)
    monkeypatch.setenv("TMUX", "/tmp/tmux-1000/default,123,0")
    monkeypatch.setattr(terminal, "_get_wezterm_bin", lambda: "/usr/bin/wezterm")
    assert terminal.detect_terminal() == "tmux"


def test_detect_terminal_does_not_select_tmux_when_not_inside_tmux(monkeypatch) -> None:
    _clear_terminal_env(monkeypatch)
    monkeypatch.setattr(terminal, "_get_wezterm_bin", lambda: None)
    assert terminal.detect_terminal() is None


def test_detect_terminal_selects_wezterm_when_available(monkeypatch) -> None:
    _clear_terminal_env(monkeypatch)
    monkeypatch.setattr(terminal, "_get_wezterm_bin", lambda: "/usr/bin/wezterm")
    assert terminal.detect_terminal() == "wezterm"
