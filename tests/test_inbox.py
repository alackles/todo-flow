import time

import pytest

import inbox


@pytest.fixture(autouse=True)
def utc(monkeypatch):
    monkeypatch.setenv("TZ", "UTC")
    time.tzset()


def msg(id, text, ts="2026-11-08T21:14:00+00:00", bot=False, type=0):
    return {"id": str(id), "content": text, "timestamp": ts, "type": type,
            "author": {"bot": bot}}


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


@pytest.fixture
def discord(monkeypatch, tmp_path):
    """A fake Discord channel and a temp inbox.md. Records deletes and commits."""
    state = {"messages": [], "deleted": [], "commits": [], "path": tmp_path / "inbox.md"}
    monkeypatch.setattr(inbox, "load_config", lambda: ("token", "123", state["path"]))
    monkeypatch.setattr(inbox, "fetch_messages", lambda token, channel: state["messages"])
    monkeypatch.setattr(inbox, "delete_message",
                        lambda token, channel, mid: state["deleted"].append(mid))
    monkeypatch.setattr(inbox, "commit_inbox", lambda path, n: state["commits"].append(n))
    return state


def test_fetch_is_oldest_first_and_skips_bots_and_system_messages(monkeypatch):
    # Discord returns newest first.
    page = [msg(30, "third"), msg(25, "bot", bot=True), msg(20, "pinned", type=6), msg(10, "first")]
    monkeypatch.setattr(inbox, "request", lambda *a, **k: FakeResponse(page))
    got = inbox.fetch_messages("token", "123")
    assert [m["content"] for m in got] == ["first", "third"]


def test_entry_has_time_hidden_id_and_indented_continuation():
    entry = inbox.format_entry(msg(10, "email the dean\nabout room booking"))
    assert entry == ("- Sun Nov 8, 9:14 PM: email the dean <!-- discord:10 -->\n"
                     "  about room booking")


def test_pull_adds_only_new_text_then_deletes_what_is_in_the_file(discord):
    # 10 is already in the file (an earlier delete failed); 30 has no text.
    discord["path"].write_text(inbox.HEADER + "\n" + inbox.format_entry(msg(10, "old")) + "\n")
    discord["messages"] = [msg(10, "old"), msg(20, "new"), msg(30, "")]
    assert inbox.cmd_pull() == 0
    text = discord["path"].read_text()
    assert text.count("discord:10") == 1
    assert "new <!-- discord:20 -->" in text
    assert "discord:30" not in text
    assert discord["deleted"] == ["10", "20"]  # the textless one stays in Discord
    assert discord["commits"] == [1]


def test_nothing_deleted_from_discord_if_the_file_write_fails(discord, monkeypatch):
    discord["messages"] = [msg(20, "new")]

    def disk_full(*a):
        raise OSError("disk full")
    monkeypatch.setattr(inbox, "add_to_inbox", disk_full)
    assert inbox.cmd_pull() == 1
    assert discord["deleted"] == []
