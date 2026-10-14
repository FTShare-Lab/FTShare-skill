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
    def test_main_prints_full_response(self, mock_fetch):
        mock_fetch.return_value = {"code": 200, "message": "success", "data": [{"stock_name": "上海医药"}]}
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}), \
                patch.object(sys, "argv", ["handler.py"]), \
                patch("sys.stdout", new_callable=StringIO) as out:
            handler.main()
        self.assertEqual(mock_fetch.call_args.args, ())
        payload = json.loads(out.getvalue())
        self.assertEqual(payload["code"], 200)
        self.assertEqual(payload["data"][0]["stock_name"], "上海医药")


if __name__ == "__main__":
    unittest.main()
