# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Microsoft Agent 365 Tooling SDK

Core tooling functionality shared across different AI frameworks.
Provides base utilities and common helper functions.
"""

from .models import AgentSettings, AgentSettingTemplate, MCPServerConfig
from .services import AgentSettingsService, McpToolServerConfigurationService
from .utils import Constants
from .utils.utility import (
    build_mcp_server_url,
    get_agent_settings_base_url,
    get_mcp_base_url,
    get_tooling_gateway_for_digital_worker,
)

__version__ = "1.0.0"

__all__ = [
    "AgentSettings",
    "AgentSettingsService",
    "AgentSettingTemplate",
    "MCPServerConfig",
    "McpToolServerConfigurationService",
    "Constants",
    "get_tooling_gateway_for_digital_worker",
    "get_mcp_base_url",
    "build_mcp_server_url",
    "get_agent_settings_base_url",
]
