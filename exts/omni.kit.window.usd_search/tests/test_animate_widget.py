import unittest


class TestAnimateWidget(unittest.TestCase):
    def test_class_imported_with_correct_spelling(self):
        from omni.kit.window.usd_search.utils.animate_widget import AnimateWidget
        self.assertTrue(callable(AnimateWidget))


if __name__ == "__main__":
