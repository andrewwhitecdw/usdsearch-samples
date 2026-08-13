# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary

import pytest
from unittest.mock import AsyncMock, patch

from omni.kit.window.usd_search.utils.ngc_connect import NgcConnect


@pytest.mark.asyncio
async def test_send_url_request_async_url_encodes_query_params():
    connect = NgcConnect()
    connect._api_key = "test-api-key"
    connect.set_payload({
        "description": "red car & truck",
        "return_metadata": False,
        "limit": 10,
        "file_extension_include": "*.usd",
        "return_images": True,
    })

    with patch("omni.kit.window.usd_search.utils.ngc_connect.aiohttp.ClientSession") as mock_session_cls:
        mock_session = AsyncMock()
        mock_session_cls.return_value.__aenter__.return_value = mock_session

        mock_response = AsyncMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = AsyncMock()
        mock_session.get.return_value.__aenter__.return_value = mock_response

        await connect.send_url_request_async("https://example.com/search")

        called_url = mock_session.get.call_args.args[0]
        assert "description=red+car+%26+truck" in called_url
