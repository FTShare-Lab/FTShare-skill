import importlib.util
import json
import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch

_DIR = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_DIR, "handler.py"))
handler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handler)

class TestHandler(unittest.TestCase):
    @patch.object(handler, "fetch")
    def test_optional_filters(self, mock_fetch):
        mock_fetch.return_value = {"code": 200, "data": []}
        with patch.object(sys, "argv", ["handler.py", "--trade-code", "600848.SH", "--change-date", "20240101", "--change-type", "上市"]), patch("sys.stdout", new_callable=StringIO) as out:
            handler.main()
        self.assertEqual(mock_fetch.call_args.args[0], {"trade_code": "600848.SH", "change_date": "20240101", "change_type": "上市"})
        self.assertEqual(json.loads(out.getvalue())["code"], 200)

if __name__ == "__main__": unittest.main()
