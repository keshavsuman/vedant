"""White-label loader and customize apply behavior."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml


@pytest.fixture
def wl_home(tmp_path, monkeypatch):
    home = tmp_path / ".keshav"
    home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(home))
    monkeypatch.setenv("KESHAV_HOME", str(home))
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    return home


def test_load_merges_repo_and_home(wl_home, monkeypatch):
    from hermes_cli import white_label as wl

    wl.clear_white_label_cache()
    repo = wl_home.parent / "repo_wl.yaml"
    repo.write_text(
        yaml.dump(
            {
                "brand": {"product_name": "RepoBot", "cli_name": "repo"},
                "tone": {"soul": "repo soul"},
                "capabilities": {"config": {"memory": {"provider": ""}}},
            }
        ),
        encoding="utf-8",
    )
    home_wl = wl_home / "white_label.yaml"
    home_wl.write_text(
        yaml.dump({"brand": {"product_name": "HomeBot"}, "tone": {"soul": "home soul"}}),
        encoding="utf-8",
    )

    monkeypatch.setattr(wl, "repo_white_label_path", lambda: repo)
    monkeypatch.setattr(
        wl, "resolve_white_label_paths", lambda: [repo, home_wl]
    )

    data = wl.load_white_label(force=True)
    assert data["brand"]["product_name"] == "HomeBot"
    assert data["brand"]["cli_name"] == "repo"
    assert data["tone"]["soul"] == "home soul"
    assert data["capabilities"]["config"]["memory"]["provider"] == ""


def test_apply_writes_soul_and_config(wl_home, monkeypatch):
    from hermes_cli import white_label as wl

    wl.clear_white_label_cache()
    repo = wl_home.parent / "repo_wl.yaml"
    repo.write_text(
        yaml.dump(
            {
                "brand": {"default_skin": "keshav", "cli_name": "tomorrow"},
                "tone": {"soul": "You are TestBot."},
                "capabilities": {
                    "config": {
                        "display": {"skin": "keshav"},
                        "memory": {"memory_enabled": True, "provider": ""},
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(wl, "repo_white_label_path", lambda: repo)
    monkeypatch.setattr(wl, "resolve_white_label_paths", lambda: [repo])

    # Minimal config stubs so apply doesn't need a full install
    cfg_path = wl_home / "config.yaml"
    cfg_path.write_text("display:\n  skin: default\n", encoding="utf-8")

    actions = wl.apply_white_label(force_soul=True, dry_run=False)
    assert any("SOUL.md" in a for a in actions)
    soul = (wl_home / "SOUL.md").read_text(encoding="utf-8")
    assert "TestBot" in soul
    assert (wl_home / "white_label.yaml").is_file()

    loaded = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
    assert loaded["display"]["skin"] == "keshav"
    assert loaded["memory"]["memory_enabled"] is True


def test_apply_skips_custom_soul_without_force(wl_home, monkeypatch):
    from hermes_cli import white_label as wl

    wl.clear_white_label_cache()
    repo = wl_home.parent / "repo_wl.yaml"
    repo.write_text(
        yaml.dump({"tone": {"soul": "from yaml"}, "brand": {"default_skin": "keshav"}}),
        encoding="utf-8",
    )
    monkeypatch.setattr(wl, "repo_white_label_path", lambda: repo)
    monkeypatch.setattr(wl, "resolve_white_label_paths", lambda: [repo])

    (wl_home / "SOUL.md").write_text("I am a custom persona.\n", encoding="utf-8")
    (wl_home / "config.yaml").write_text("{}\n", encoding="utf-8")

    actions = wl.apply_white_label(force_soul=False, dry_run=False)
    assert any("skip customized" in a for a in actions)
    assert (wl_home / "SOUL.md").read_text(encoding="utf-8") == "I am a custom persona.\n"
