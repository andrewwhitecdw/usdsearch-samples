# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import pytest
from unittest.mock import patch

from omni.kit.window.usd_search.utils.ngc_connect import NgcConnect


class _FakeSettings:
    def get(self, key, default=None):
        if key.endswith("require_authorization"):
            return False
        return default


class _FakeResponse:
    async def json(self):
        return []

    def raise_for_status(self):
        pass


class _FakePostContext:
    async def __aenter__(self):
        return _FakeResponse()

    async def __aexit__(self, exc_type, exc, tb):
        return False


class _FakeSession:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    def post(self, *args, **kwargs):
        return _FakePostContext()

    def get(self, *args, **kwargs):
        return _FakePostContext()


@pytest.mark.asyncio
async def test_payload_dict_preserved_across_repeated_calls():
    payload = {"description": "unit test", "limit": 5}
    nc = NgcConnect()
    nc._settings = _FakeSettings()
    nc.set_payload(payload)

    with patch("omni.kit.window.usd_search.utils.ngc_connect.aiohttp.ClientSession", _FakeSession):
        await nc.send_api_request_async("https://example.com/api")
        assert isinstance(nc._payload, dict)

        await nc.send_api_request_async("https://example.com/api")
        assert isinstance(nc._payload, dict)
        assert nc._payload == payload

        await nc.send_url_request_async("https://example.com/url")
        assert isinstance(nc._payload, dict)
