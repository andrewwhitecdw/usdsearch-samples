import unittest

from omni.kit.window.usd_search.utils.animate_widget import AnimateWidget
from omni.kit.window.usd_search.utils.animate_widget import AnimateWindget


class TestAnimateWidget(unittest.TestCase):
    def test_class_name_typo_fixed(self):
        self.assertEqual(AnimateWidget.__name__, "AnimateWidget")

    def test_backward_compatible_alias(self):
        self.assertIs(AnimateWindget, AnimateWidget)
