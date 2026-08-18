import ast
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


class TestNoCallbackAccumulation(unittest.TestCase):
    def test_model_callbacks_not_registered_inside_rebuild(self):
        with open(_get_window_source_path(), "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        rebuild = None
        for node in ast.walk(tree):
            if isinstance(node, ast.AsyncFunctionDef) and node.name == "_rebuild_ui_async":
                rebuild = node
                break
        self.assertIsNotNone(rebuild, "_rebuild_ui_async must exist")

        source = ast.unparse(rebuild)
        for name in (
            "add_begin_edit_fn",
            "add_end_edit_fn",
            "add_value_changed_fn",
        ):
            self.assertNotIn(
                name,
                source,
                f"{name} must not be called inside _rebuild_ui_async; register once in __init__ instead",
            )
