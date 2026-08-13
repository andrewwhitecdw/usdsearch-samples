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
from unittest.mock import MagicMock, patch

from omni.kit.window.usd_search.window import UsdSearchWindow


class _Model:
    def __init__(self, asset_url, asset_name):
        self.asset_url = asset_url
        self.asset_name = asset_name


class TestOnClickImage(unittest.TestCase):
    @patch("omni.kit.window.usd_search.window.logger")
    def test_skips_when_model_is_none(self, mock_logger):
        UsdSearchWindow.on_click_image(None, None)
        mock_logger.warning.assert_called_once_with(
            "Skipping image click: missing asset metadata"
        )

    @patch("omni.kit.window.usd_search.window.logger")
    def test_skips_when_asset_url_is_missing(self, mock_logger):
        model = _Model(asset_url=None, asset_name="foo.usd")
        UsdSearchWindow.on_click_image(None, model)
        mock_logger.warning.assert_called_once_with(
            "Skipping image click: missing asset metadata"
        )

    @patch("omni.kit.window.usd_search.window.logger")
    def test_skips_when_asset_name_is_missing(self, mock_logger):
        model = _Model(asset_url="http://x/foo.usd", asset_name=None)
        UsdSearchWindow.on_click_image(None, model)
        mock_logger.warning.assert_called_once_with(
            "Skipping image click: missing asset metadata"
        )

    @patch("omni.kit.commands.execute")
    @patch("omni.usd.get_stage_next_free_path")
    @patch("omni.usd.get_context")
    def test_proceeds_with_valid_model(self, mock_get_context, mock_next_path, mock_execute):
        stage = MagicMock()
        mock_get_context.return_value.get_stage.return_value = stage
        mock_next_path.return_value = "/foo"

        model = _Model(asset_url="http://x/foo.usd", asset_name="foo.usd")
        UsdSearchWindow.on_click_image(None, model)

        mock_execute.assert_called_once()
        mock_next_path.assert_called_once_with(stage, "/foo", True)


if __name__ == "__main__":
    unittest.main()
