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
    @patch.object(handler, "safe_urlopen")
    def test_n_is_encoded_and_json_emitted(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"code": 200, "data": {"n": 5}}'
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}), patch.object(sys, "argv", ["handler.py", "--n", "5"]), patch("sys.stdout", new_callable=StringIO) as out:
            handler.main()
        request = mock_open.call_args.args[0]
        self.assertIn("n=5", request.full_url)
        self.assertEqual(json.loads(out.getvalue())["data"]["n"], 5)

if __name__ == "__main__": unittest.main()
