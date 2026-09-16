from __future__ import annotations

import importlib.util
import io
import json
import sys
import urllib.error
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest


HANDLER = Path(__file__).with_name("handler.py")


def load_handler():
    spec = importlib.util.spec_from_file_location("financial_calendar_handler", HANDLER)
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


def test_main_forwards_documented_query(monkeypatch, capsys):
    module = load_handler()
    opened = []
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "handler.py",
            "--start-date",
            "2026-07-16",
            "--end-date",
            "2026-07-17",
            "--category",
            "economic",
            "--page",
            "1",
            "--page-size",
            "5",
        ],
    )
    monkeypatch.setattr(module, "safe_urlopen", lambda request: opened.append(request) or Response({"data": {"records": []}}))

    module.main()

    parsed = urlparse(opened[0].full_url)
    assert parsed.path == "/gateway/api/v1/market/data/finance/financial-calendar/baidu"
    assert parse_qs(parsed.query) == {
        "start_date": ["2026-07-16"],
        "end_date": ["2026-07-17"],
        "category": ["economic"],
        "page": ["1"],
        "page_size": ["5"],
    }
    assert json.loads(capsys.readouterr().out) == {"data": {"records": []}}


def test_empty_http_error_body_still_reports_status(monkeypatch, capsys):
    module = load_handler()
    monkeypatch.setattr(sys, "argv", ["handler.py", "--start-date", "2026-07-16", "--end-date", "2026-07-17"])
    error = urllib.error.HTTPError("https://example.invalid", 503, "unavailable", {}, io.BytesIO(b""))
    monkeypatch.setattr(module, "safe_urlopen", lambda request: (_ for _ in ()).throw(error))

    with pytest.raises(SystemExit):
        module.main()

    assert capsys.readouterr().err.strip() == "HTTP 503"
