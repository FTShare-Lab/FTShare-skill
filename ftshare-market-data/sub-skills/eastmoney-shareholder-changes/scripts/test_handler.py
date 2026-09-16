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
    def test_symbol_and_paging(self, mock_fetch):
        mock_fetch.return_value = {"code": 200, "data": {"pages": 1, "records": []}}
        with patch.object(sys, "argv", ["handler.py", "--symbol", "股东减持", "--page", "2", "--page-size", "20"]), patch("sys.stdout", new_callable=StringIO) as out:
            handler.main()
        self.assertEqual(mock_fetch.call_args.args[0], {"symbol": "股东减持", "page": 2, "page_size": 20})
        self.assertEqual(json.loads(out.getvalue())["code"], 200)

if __name__ == "__main__": unittest.main()
