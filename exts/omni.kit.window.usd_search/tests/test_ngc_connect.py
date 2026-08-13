# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from omni.kit.window.usd_search.utils.ngc_connect import NgcConnect


@pytest.fixture
def connect():
    return NgcConnect()


@pytest.mark.asyncio
async def test_send_url_request_async_populates_api_key_and_sets_bearer_header(connect):
    """send_url_request_async must populate _api_key before building headers so 'Bearer None' is never sent."""
    connect.set_payload({
        "description": "test query",
        "return_metadata": "False",
        "limit": "30",
        "file_extension_include": "",
        "return_images": "True",
    })

    mock_settings = MagicMock()
    mock_settings.get.side_effect = lambda key: (
        "test-api-key" if key == "/exts/omni.kit.window.usd_search/nvidia_api_key" else None
    )
    connect._settings = mock_settings

    response = AsyncMock()
    response.json.return_value = []
    response.raise_for_status = MagicMock()
    response_cm = AsyncMock()
    response_cm.__aenter__.return_value = response
    response_cm.__aexit__.return_value = False

    session = MagicMock()
    session.get.return_value = response_cm
    session_cm = AsyncMock()
    session_cm.__aenter__.return_value = session
    session_cm.__aexit__.return_value = False

    with patch(
        "omni.kit.window.usd_search.utils.ngc_connect.aiohttp.ClientSession",
        return_value=session_cm,
    ):
        await connect.send_url_request_async("https://ai.api.nvidia.com/v1/search")

    assert connect._api_key == "test-api-key"
    assert connect._headers == {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer test-api-key",
    }
