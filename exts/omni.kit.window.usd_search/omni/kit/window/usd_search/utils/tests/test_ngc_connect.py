# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from omni.kit.window.usd_search.utils.ngc_connect import NgcConnect


@pytest.fixture
def ngc_connect():
    with patch("omni.kit.window.usd_search.utils.ngc_connect.carb.settings.get_settings") as mock_settings:
        mock_settings.return_value = MagicMock()
        mock_settings.return_value.get.return_value = None
        with patch("omni.kit.window.usd_search.utils.ngc_connect.omni.client"):
            return NgcConnect()


@pytest.mark.asyncio
async def test_send_api_request_async_does_not_mutate_payload(ngc_connect):
    """Verify that send_api_request_async leaves self._payload as a dict."""
    payload = {"description": "test query", "limit": "10"}
    ngc_connect.set_payload(payload)
    ngc_connect._api_key = "fake-api-key"

    mock_response = MagicMock()
    mock_response.json = AsyncMock(return_value=[])
    mock_response.raise_for_status = MagicMock()
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)

    mock_session = MagicMock()
    mock_session.post.return_value = mock_response
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    with patch("omni.kit.window.usd_search.utils.ngc_connect.aiohttp.ClientSession", return_value=mock_session):
        result = await ngc_connect.send_api_request_async("https://ai.api.nvidia.com/v1/test")

    # Payload must remain the original dict so later calls can use .get()
    assert ngc_connect._payload is payload
    assert isinstance(ngc_connect._payload, dict)
    assert ngc_connect._payload.get("description") == "test query"

    # Request was still sent with the JSON-serialized body
    mock_session.post.assert_called_once()
    call_kwargs = mock_session.post.call_args.kwargs
    assert "data" in call_kwargs
    assert call_kwargs["data"] == '{"description": "test query", "limit": "10"}'
