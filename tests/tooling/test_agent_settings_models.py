# Copyright (c) Microsoft. All rights reserved.

"""Unit tests for Agent Settings models."""

import pytest
from microsoft_agents_a365.tooling.models.agent_settings import (
    AgentSettings,
    AgentSettingTemplate,
)


# Tests for AgentSettingTemplate
class TestAgentSettingTemplate:
    """Tests for AgentSettingTemplate model."""

    def test_create_template_with_valid_data(self):
        """Test creating a template with valid data."""
        template = AgentSettingTemplate(
            agent_type="DeclarativeAgent", settings={"key": "value"}
        )
        assert template.agent_type == "DeclarativeAgent"
        assert template.settings == {"key": "value"}

    def test_create_template_with_empty_settings(self):
        """Test creating a template with empty settings."""
        template = AgentSettingTemplate(agent_type="EntraEmbodied", settings={})
        assert template.agent_type == "EntraEmbodied"
        assert template.settings == {}

    def test_create_template_with_none_settings(self):
        """Test creating a template with None settings defaults to empty dict."""
        template = AgentSettingTemplate(agent_type="TestAgent", settings=None)
        assert template.settings == {}

    def test_create_template_without_settings(self):
        """Test creating a template without settings parameter."""
        template = AgentSettingTemplate(agent_type="TestAgent")
        assert template.agent_type == "TestAgent"
        assert template.settings == {}

    def test_create_template_with_empty_agent_type_raises(self):
        """Test that empty agent_type raises ValueError."""
        with pytest.raises(ValueError, match="agent_type cannot be empty"):
            AgentSettingTemplate(agent_type="", settings={})

    def test_create_template_with_complex_settings(self):
        """Test creating a template with complex nested settings."""
        complex_settings = {
            "feature1": {"enabled": True, "config": {"timeout": 30}},
            "feature2": ["option1", "option2"],
            "numeric": 42,
        }
        template = AgentSettingTemplate(
            agent_type="ComplexAgent", settings=complex_settings
        )
        assert template.settings == complex_settings


# Tests for AgentSettings
class TestAgentSettings:
    """Tests for AgentSettings model."""

    def test_create_settings_with_valid_data(self):
        """Test creating settings with valid data."""
        settings = AgentSettings(
            agent_instance_id="instance-123",
            agent_type="DeclarativeAgent",
            settings={"key": "value"},
        )
        assert settings.agent_instance_id == "instance-123"
        assert settings.agent_type == "DeclarativeAgent"
        assert settings.settings == {"key": "value"}

    def test_create_settings_without_agent_type(self):
        """Test creating settings without agent_type."""
        settings = AgentSettings(
            agent_instance_id="instance-456", settings={"setting": "value"}
        )
        assert settings.agent_instance_id == "instance-456"
        assert settings.agent_type is None
        assert settings.settings == {"setting": "value"}

    def test_create_settings_with_empty_settings(self):
        """Test creating settings with empty settings dict."""
        settings = AgentSettings(agent_instance_id="instance-789", settings={})
        assert settings.agent_instance_id == "instance-789"
        assert settings.settings == {}

    def test_create_settings_with_none_settings(self):
        """Test creating settings with None settings defaults to empty dict."""
        settings = AgentSettings(agent_instance_id="instance-abc", settings=None)
        assert settings.settings == {}

    def test_create_settings_without_settings_param(self):
        """Test creating settings without settings parameter."""
        settings = AgentSettings(agent_instance_id="instance-def")
        assert settings.agent_instance_id == "instance-def"
        assert settings.settings == {}

    def test_create_settings_with_empty_instance_id_raises(self):
        """Test that empty agent_instance_id raises ValueError."""
        with pytest.raises(ValueError, match="agent_instance_id cannot be empty"):
            AgentSettings(agent_instance_id="", settings={})

    def test_create_settings_with_complex_settings(self):
        """Test creating settings with complex nested settings."""
        complex_settings = {
            "preferences": {"theme": "dark", "language": "en"},
            "features": ["feature1", "feature2"],
            "limits": {"maxTokens": 1000, "timeout": 60},
        }
        settings = AgentSettings(
            agent_instance_id="complex-instance",
            agent_type="ComplexAgent",
            settings=complex_settings,
        )
        assert settings.settings == complex_settings
