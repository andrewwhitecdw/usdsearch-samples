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


class TestWindowImports(unittest.TestCase):
    def test_all_used_omni_modules_are_imported(self):
        with open(_get_window_source_path(), "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported.add(node.module)

        used = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                inner = node.value
                parts = [node.attr]
                while isinstance(inner, ast.Attribute):
                    parts.append(inner.attr)
                    inner = inner.value
                if isinstance(inner, ast.Name) and inner.id == "omni":
                    parts.append("omni")
                    parts.reverse()
                    for i in range(1, len(parts)):
                        used.add(".".join(parts[: i + 1]))

        required = {"omni.appwindow", "omni.kit.app", "omni.kit.commands", "omni.usd"}
        missing = required - imported
        self.assertFalse(
            missing,
            f"The following omni modules are used but not imported: {sorted(missing)}",
        )
