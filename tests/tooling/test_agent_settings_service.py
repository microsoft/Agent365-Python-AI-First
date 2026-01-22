# Copyright (c) Microsoft. All rights reserved.

"""Unit tests for Agent Settings Service."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from microsoft_agents_a365.tooling.services.agent_settings_service import (
    AgentSettingsService,
)


@pytest.fixture
def agent_settings_service():
    """Fixture to create AgentSettingsService instance."""
    return AgentSettingsService()


@pytest.fixture
def mock_auth_token():
    """Fixture for a mock authentication token."""
    return "test-auth-token-123"


# Tests for input validation
class TestAgentSettingsServiceValidation:
    """Tests for AgentSettingsService input validation."""

    @pytest.mark.asyncio
    async def test_get_setting_template_empty_agent_type_raises(
        self, agent_settings_service, mock_auth_token
    ):
        """Test that empty agent_type raises ValueError."""
        with pytest.raises(ValueError, match="agent_type cannot be empty"):
            await agent_settings_service.get_setting_template("", mock_auth_token)

    @pytest.mark.asyncio
    async def test_get_setting_template_empty_auth_token_raises(
        self, agent_settings_service
    ):
        """Test that empty auth_token raises ValueError."""
        with pytest.raises(ValueError, match="auth_token cannot be empty"):
            await agent_settings_service.get_setting_template("TestAgent", "")

    @pytest.mark.asyncio
    async def test_set_setting_template_empty_agent_type_raises(
        self, agent_settings_service, mock_auth_token
    ):
        """Test that empty agent_type raises ValueError for set operation."""
        with pytest.raises(ValueError, match="agent_type cannot be empty"):
            await agent_settings_service.set_setting_template(
                "", {"key": "value"}, mock_auth_token
            )

    @pytest.mark.asyncio
    async def test_get_agent_settings_empty_instance_id_raises(
        self, agent_settings_service, mock_auth_token
    ):
        """Test that empty agent_instance_id raises ValueError."""
        with pytest.raises(ValueError, match="agent_instance_id cannot be empty"):
            await agent_settings_service.get_agent_settings("", mock_auth_token)

    @pytest.mark.asyncio
    async def test_set_agent_settings_empty_instance_id_raises(
        self, agent_settings_service, mock_auth_token
    ):
        """Test that empty agent_instance_id raises ValueError for set operation."""
        with pytest.raises(ValueError, match="agent_instance_id cannot be empty"):
            await agent_settings_service.set_agent_settings(
                "", {"key": "value"}, mock_auth_token
            )


# Tests for template operations
class TestAgentSettingsServiceTemplateOperations:
    """Tests for AgentSettingsService template operations."""

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession")
    async def test_get_setting_template_success(
        self, mock_session_class, agent_settings_service, mock_auth_token
    ):
        """Test successful retrieval of setting template."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(
            return_value=json.dumps(
                {"agentType": "DeclarativeAgent", "settings": {"feature": "enabled"}}
            )
        )

        mock_session = MagicMock()
        mock_session.get = MagicMock(return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response)))
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        mock_session_class.return_value = mock_session

        result = await agent_settings_service.get_setting_template(
            "DeclarativeAgent", mock_auth_token
        )

        assert result.agent_type == "DeclarativeAgent"
        assert result.settings == {"feature": "enabled"}

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession")
    async def test_get_setting_template_not_found_returns_empty(
        self, mock_session_class, agent_settings_service, mock_auth_token
    ):
        """Test that 404 response returns empty template."""
        mock_response = AsyncMock()
        mock_response.status = 404

        mock_session = MagicMock()
        mock_session.get = MagicMock(return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response)))
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        mock_session_class.return_value = mock_session

        result = await agent_settings_service.get_setting_template(
            "NonExistentAgent", mock_auth_token
        )

        assert result.agent_type == "NonExistentAgent"
        assert result.settings == {}

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession")
    async def test_set_setting_template_success(
        self, mock_session_class, agent_settings_service, mock_auth_token
    ):
        """Test successful setting of template."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(
            return_value=json.dumps(
                {"agentType": "TestAgent", "settings": {"newSetting": "value"}}
            )
        )

        mock_session = MagicMock()
        mock_session.put = MagicMock(return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response)))
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        mock_session_class.return_value = mock_session

        result = await agent_settings_service.set_setting_template(
            "TestAgent", {"newSetting": "value"}, mock_auth_token
        )

        assert result.agent_type == "TestAgent"
        assert result.settings == {"newSetting": "value"}


# Tests for instance operations
class TestAgentSettingsServiceInstanceOperations:
    """Tests for AgentSettingsService instance operations."""

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession")
    async def test_get_agent_settings_success(
        self, mock_session_class, agent_settings_service, mock_auth_token
    ):
        """Test successful retrieval of agent settings."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(
            return_value=json.dumps(
                {
                    "agentInstanceId": "instance-123",
                    "agentType": "TestAgent",
                    "settings": {"preference": "dark"},
                }
            )
        )

        mock_session = MagicMock()
        mock_session.get = MagicMock(return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response)))
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        mock_session_class.return_value = mock_session

        result = await agent_settings_service.get_agent_settings(
            "instance-123", mock_auth_token
        )

        assert result.agent_instance_id == "instance-123"
        assert result.agent_type == "TestAgent"
        assert result.settings == {"preference": "dark"}

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession")
    async def test_get_agent_settings_not_found_returns_empty(
        self, mock_session_class, agent_settings_service, mock_auth_token
    ):
        """Test that 404 response returns empty settings."""
        mock_response = AsyncMock()
        mock_response.status = 404

        mock_session = MagicMock()
        mock_session.get = MagicMock(return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response)))
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        mock_session_class.return_value = mock_session

        result = await agent_settings_service.get_agent_settings(
            "nonexistent-instance", mock_auth_token
        )

        assert result.agent_instance_id == "nonexistent-instance"
        assert result.settings == {}

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession")
    async def test_set_agent_settings_success(
        self, mock_session_class, agent_settings_service, mock_auth_token
    ):
        """Test successful setting of agent settings."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(
            return_value=json.dumps(
                {
                    "agentInstanceId": "instance-456",
                    "agentType": "CustomAgent",
                    "settings": {"config": "updated"},
                }
            )
        )

        mock_session = MagicMock()
        mock_session.put = MagicMock(return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response)))
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        mock_session_class.return_value = mock_session

        result = await agent_settings_service.set_agent_settings(
            "instance-456", {"config": "updated"}, mock_auth_token, agent_type="CustomAgent"
        )

        assert result.agent_instance_id == "instance-456"
        assert result.agent_type == "CustomAgent"
        assert result.settings == {"config": "updated"}

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession")
    async def test_set_agent_settings_created_status(
        self, mock_session_class, agent_settings_service, mock_auth_token
    ):
        """Test that 201 status is handled correctly."""
        mock_response = AsyncMock()
        mock_response.status = 201
        mock_response.text = AsyncMock(
            return_value=json.dumps(
                {
                    "agentInstanceId": "new-instance",
                    "settings": {"initial": "setting"},
                }
            )
        )

        mock_session = MagicMock()
        mock_session.put = MagicMock(return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response)))
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        mock_session_class.return_value = mock_session

        result = await agent_settings_service.set_agent_settings(
            "new-instance", {"initial": "setting"}, mock_auth_token
        )

        assert result.agent_instance_id == "new-instance"
        assert result.settings == {"initial": "setting"}
