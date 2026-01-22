# Copyright (c) Microsoft. All rights reserved.

"""Unit tests for Agent Settings utility functions."""

import os
from unittest.mock import patch

from microsoft_agents_a365.tooling.utils.utility import (
    get_agent_settings_base_url,
)


class TestAgentSettingsUtility:
    """Tests for agent settings utility functions."""

    def test_get_agent_settings_base_url_default(self):
        """Test that default base URL is returned when env var is not set."""
        with patch.dict(os.environ, {}, clear=True):
            # Remove MCP_PLATFORM_ENDPOINT if it exists
            os.environ.pop("MCP_PLATFORM_ENDPOINT", None)
            url = get_agent_settings_base_url()
            assert url == "https://agent365.svc.cloud.microsoft/agents/settings"

    def test_get_agent_settings_base_url_with_env_var(self):
        """Test that custom base URL is used when env var is set."""
        with patch.dict(
            os.environ, {"MCP_PLATFORM_ENDPOINT": "https://custom.endpoint.com"}
        ):
            url = get_agent_settings_base_url()
            assert url == "https://custom.endpoint.com/agents/settings"

    def test_get_agent_settings_base_url_with_empty_env_var(self):
        """Test behavior with empty env var - follows existing _get_mcp_platform_base_url behavior."""
        with patch.dict(os.environ, {"MCP_PLATFORM_ENDPOINT": ""}):
            url = get_agent_settings_base_url()
            # Empty string from env var is used as-is (consistent with existing behavior)
            assert url == "/agents/settings"
