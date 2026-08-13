# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import unittest

from omni.kit.window.usd_search.window import UsdSearchWindow


class TestUsdSearchWindow(unittest.TestCase):
    def test_default_search_models_not_shared(self):
        """Regression test for mutable default argument leak in UsdSearchWindow."""
        window1 = UsdSearchWindow("Window 1")
        window2 = UsdSearchWindow("Window 2")

        self.assertIsNot(window1._search_models, window2._search_models)

        window1._search_models.append("leaked_item")
        self.assertNotIn("leaked_item", window2._search_models)


