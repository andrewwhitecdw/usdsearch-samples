import os
import unittest


def _get_window_source_path():
    return os.path.join(
        os.path.dirname(__file__),
        "..",
        "omni",
        "kit",
        "window",
        "usd_search",
        "window.py",
    )


class TestApiErrorHandling(unittest.TestCase):
    def test_no_literal_error_string_comparison(self):
        with open(_get_window_source_path(), "r", encoding="utf-8") as f:
            source = f.read()
        self.assertNotIn(
            'bundle == "error"',
            source,
            "Comparing the response bundle to the literal string 'error' is incorrect; "
            "use a key-based check such as 'error' in bundle.",
        )


