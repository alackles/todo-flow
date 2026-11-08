import time

import pytest

import inbox


@pytest.fixture(autouse=True)
def utc(monkeypatch):
    monkeypatch.setenv("TZ", "UTC")
    time.tzset()


@pytest.fixture
def config(monkeypatch):
    monkeypatch.setattr(inbox, "load_config", lambda: ("token", "123"))


def msg(id, text, ts="2026-11-08T21:14:00+00:00", bot=False, type=0):
    return {"id": str(id), "content": text, "timestamp": ts, "type": type,
            "author": {"bot": bot}}


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


def test_fetch_is_oldest_first_and_skips_bots_and_system_messages(monkeypatch):
    # Discord returns newest first.
    page = [msg(30, "third"), msg(25, "bot", bot=True), msg(20, "pinned", type=6), msg(10, "first")]
    monkeypatch.setattr(inbox, "request", lambda *a, **k: FakeResponse(page))
    got = inbox.fetch_messages("token", "123")
    assert [m["content"] for m in got] == ["first", "third"]


def test_format_shows_id_time_and_indents_multiline():
    out = inbox.format_pull([msg(10, "email the dean\nabout room booking")])
    assert "[10] Sun Nov 8, 9:14 PM: email the dean\n    about room booking" in out


def test_empty_inbox_says_so():
    assert inbox.format_pull([]) == "Discord inbox: empty."


def test_pull_fails_soft(monkeypatch, config, capsys):
    def boom(*a):
        raise ConnectionError("no network")
    monkeypatch.setattr(inbox, "fetch_messages", boom)
    assert inbox.cmd_pull() == 0
    assert "still safe in Discord" in capsys.readouterr().out


def test_ack_continues_past_a_failure(monkeypatch, config, capsys):
    deleted = []

    def delete(token, channel, mid):
        if mid == "2":
            raise inbox.InboxError("Discord said HTTP 403", status=403)
        deleted.append(mid)
        return True
    monkeypatch.setattr(inbox, "delete_message", delete)
    assert inbox.cmd_ack(["1", "2", "3"]) == 1
    assert deleted == ["1", "3"]
    assert "[2] FAILED, still in Discord" in capsys.readouterr().out
