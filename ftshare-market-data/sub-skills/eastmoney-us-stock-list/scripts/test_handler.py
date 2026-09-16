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
    def test_contract_and_json(self, mock_fetch):
        mock_fetch.return_value = {"code": 200, "data": {"pages": 1, "records": []}}
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}), patch.object(sys, "argv", ["handler.py", "--refresh", "--page", "2", "--page-size", "5"]), patch("sys.stdout", new_callable=StringIO) as out:
            handler.main()
        self.assertEqual(mock_fetch.call_args.args[0], {"page": 2, "refresh": "true", "page_size": 5})
        self.assertEqual(json.loads(out.getvalue())["code"], 200)

if __name__ == "__main__": unittest.main()
