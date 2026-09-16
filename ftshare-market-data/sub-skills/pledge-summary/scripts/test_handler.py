from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest


HANDLER = Path(__file__).with_name("handler.py")


def load_handler():
    spec = importlib.util.spec_from_file_location("pledge_summary_handler", HANDLER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class Response:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def read(self):
        return json.dumps(self.payload).encode()


def test_main_preserves_paginated_envelope(monkeypatch, capsys):
    module = load_handler()
    opened = []
    payload = {
        "code": 0,
        "message": "success",
        "data": {"pageNum": 1, "pageSize": 5, "total": 1, "pages": 1, "records": [{"trade_date": "2026-07-17", "pledge_total_ratio": "0.1250"}]},
    }
    monkeypatch.setattr(sys, "argv", ["handler.py", "--page", "1", "--page-size", "5"])
    monkeypatch.setattr(module, "safe_urlopen", lambda request: opened.append(request) or Response(payload))

    module.main()

    parsed = urlparse(opened[0].full_url)
    assert parsed.path == "/gateway/api/v1/market/data/pledge/pledge-summary"
    assert parse_qs(parsed.query) == {"page": ["1"], "page_size": ["5"]}
    assert json.loads(capsys.readouterr().out) == payload


def test_main_accepts_empty_records(monkeypatch, capsys):
    module = load_handler()
    payload = {"code": 0, "message": "success", "data": {"records": []}}
    monkeypatch.setattr(sys, "argv", ["handler.py"])
    monkeypatch.setattr(module, "safe_urlopen", lambda request: Response(payload))

    module.main()

    assert json.loads(capsys.readouterr().out) == payload


def test_main_rejects_unexpected_response_shape(monkeypatch, capsys):
    module = load_handler()
    monkeypatch.setattr(sys, "argv", ["handler.py"])
    monkeypatch.setattr(module, "safe_urlopen", lambda request: Response(["unexpected"]))

    with pytest.raises(SystemExit):
        module.main()

    assert json.loads(capsys.readouterr().err) == {"error": "unexpected response shape"}
