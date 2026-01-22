# Copyright (c) Microsoft. All rights reserved.

"""
Agent Settings Configuration Service.

This module provides the implementation of the Agent Settings Configuration Service
that communicates with the agent settings API to manage agent setting templates
and agent instance settings.

The service supports operations for:
- Getting and setting agent setting templates by agent type
- Getting and setting agent settings by agent instance
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

# Standard library imports
import json
import logging
from typing import Any, Dict, Optional

# Third-party imports
import aiohttp

# Local imports
from ..models import ToolOptions
from ..models.agent_settings import AgentSettings, AgentSettingTemplate
from ..utils import Constants
from ..utils.utility import get_agent_settings_base_url

# Runtime Imports
from microsoft_agents_a365.runtime.utility import Utility as RuntimeUtility


# ==============================================================================
# MAIN SERVICE CLASS
# ==============================================================================


class AgentSettingsService:
    """
    Provides services for agent settings management.

    This service handles operations for agent setting templates (by agent type)
    and agent instance settings through the Agent365 platform API.
    """

    # --------------------------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------------------------

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the Agent Settings Service.

        Args:
            logger: Logger instance for logging operations. If None, creates a new logger.
        """
        self._logger = logger or logging.getLogger(self.__class__.__name__)

    # --------------------------------------------------------------------------
    # PUBLIC API - TEMPLATE OPERATIONS (BY AGENT TYPE)
    # --------------------------------------------------------------------------

    async def get_setting_template(
        self, agent_type: str, auth_token: str, options: Optional[ToolOptions] = None
    ) -> AgentSettingTemplate:
        """
        Gets the agent setting template for a specific agent type.

        Args:
            agent_type: The agent type identifier (e.g., "DeclarativeAgent").
            auth_token: Authentication token to access the API.
            options: Optional ToolOptions instance containing optional parameters.

        Returns:
            AgentSettingTemplate: The setting template for the specified agent type.

        Raises:
            ValueError: If required parameters are invalid or empty.
            Exception: If there's an error communicating with the API.
        """
        self._validate_agent_type(agent_type)
        self._validate_auth_token(auth_token)

        if options is None:
            options = ToolOptions(orchestrator_name=None)

        endpoint = f"{get_agent_settings_base_url()}/templates/{agent_type}"
        headers = self._prepare_headers(auth_token, options)

        self._logger.info(f"Getting setting template for agent type: {agent_type}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, headers=headers) as response:
                    if response.status == 200:
                        data = await self._parse_json_response(response)
                        return AgentSettingTemplate(
                            agent_type=data.get("agentType", agent_type),
                            settings=data.get("settings", {}),
                        )
                    elif response.status == 404:
                        # Return empty template if not found
                        return AgentSettingTemplate(agent_type=agent_type, settings={})
                    else:
                        raise Exception(f"HTTP {response.status}: {await response.text()}")

        except aiohttp.ClientError as http_ex:
            error_msg = f"Failed to get setting template for agent type {agent_type}: {str(http_ex)}"
            self._logger.error(error_msg)
            raise Exception(error_msg) from http_ex

    async def set_setting_template(
        self,
        agent_type: str,
        settings: Dict[str, Any],
        auth_token: str,
        options: Optional[ToolOptions] = None,
    ) -> AgentSettingTemplate:
        """
        Sets the agent setting template for a specific agent type.

        Args:
            agent_type: The agent type identifier (e.g., "DeclarativeAgent").
            settings: The settings dictionary to set as the template.
            auth_token: Authentication token to access the API.
            options: Optional ToolOptions instance containing optional parameters.

        Returns:
            AgentSettingTemplate: The updated setting template.

        Raises:
            ValueError: If required parameters are invalid or empty.
            Exception: If there's an error communicating with the API.
        """
        self._validate_agent_type(agent_type)
        self._validate_auth_token(auth_token)

        if options is None:
            options = ToolOptions(orchestrator_name=None)

        endpoint = f"{get_agent_settings_base_url()}/templates/{agent_type}"
        headers = self._prepare_headers(auth_token, options)
        headers["Content-Type"] = "application/json"

        payload = {"agentType": agent_type, "settings": settings or {}}

        self._logger.info(f"Setting template for agent type: {agent_type}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.put(
                    endpoint, headers=headers, json=payload
                ) as response:
                    if response.status in (200, 201):
                        data = await self._parse_json_response(response)
                        return AgentSettingTemplate(
                            agent_type=data.get("agentType", agent_type),
                            settings=data.get("settings", settings),
                        )
                    else:
                        raise Exception(f"HTTP {response.status}: {await response.text()}")

        except aiohttp.ClientError as http_ex:
            error_msg = f"Failed to set setting template for agent type {agent_type}: {str(http_ex)}"
            self._logger.error(error_msg)
            raise Exception(error_msg) from http_ex

    # --------------------------------------------------------------------------
    # PUBLIC API - INSTANCE OPERATIONS (BY AGENT INSTANCE)
    # --------------------------------------------------------------------------

    async def get_agent_settings(
        self, agent_instance_id: str, auth_token: str, options: Optional[ToolOptions] = None
    ) -> AgentSettings:
        """
        Gets the settings for a specific agent instance.

        Args:
            agent_instance_id: The unique identifier for the agent instance.
            auth_token: Authentication token to access the API.
            options: Optional ToolOptions instance containing optional parameters.

        Returns:
            AgentSettings: The settings for the specified agent instance.

        Raises:
            ValueError: If required parameters are invalid or empty.
            Exception: If there's an error communicating with the API.
        """
        self._validate_agent_instance_id(agent_instance_id)
        self._validate_auth_token(auth_token)

        if options is None:
            options = ToolOptions(orchestrator_name=None)

        endpoint = f"{get_agent_settings_base_url()}/instances/{agent_instance_id}"
        headers = self._prepare_headers(auth_token, options)

        self._logger.info(f"Getting settings for agent instance: {agent_instance_id}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, headers=headers) as response:
                    if response.status == 200:
                        data = await self._parse_json_response(response)
                        return AgentSettings(
                            agent_instance_id=data.get("agentInstanceId", agent_instance_id),
                            agent_type=data.get("agentType"),
                            settings=data.get("settings", {}),
                        )
                    elif response.status == 404:
                        # Return empty settings if not found
                        return AgentSettings(
                            agent_instance_id=agent_instance_id, settings={}
                        )
                    else:
                        raise Exception(f"HTTP {response.status}: {await response.text()}")

        except aiohttp.ClientError as http_ex:
            error_msg = (
                f"Failed to get settings for agent instance {agent_instance_id}: {str(http_ex)}"
            )
            self._logger.error(error_msg)
            raise Exception(error_msg) from http_ex

    async def set_agent_settings(
        self,
        agent_instance_id: str,
        settings: Dict[str, Any],
        auth_token: str,
        agent_type: Optional[str] = None,
        options: Optional[ToolOptions] = None,
    ) -> AgentSettings:
        """
        Sets the settings for a specific agent instance.

        Args:
            agent_instance_id: The unique identifier for the agent instance.
            settings: The settings dictionary to set for the agent instance.
            auth_token: Authentication token to access the API.
            agent_type: Optional agent type identifier.
            options: Optional ToolOptions instance containing optional parameters.

        Returns:
            AgentSettings: The updated settings for the agent instance.

        Raises:
            ValueError: If required parameters are invalid or empty.
            Exception: If there's an error communicating with the API.
        """
        self._validate_agent_instance_id(agent_instance_id)
        self._validate_auth_token(auth_token)

        if options is None:
            options = ToolOptions(orchestrator_name=None)

        endpoint = f"{get_agent_settings_base_url()}/instances/{agent_instance_id}"
        headers = self._prepare_headers(auth_token, options)
        headers["Content-Type"] = "application/json"

        payload: Dict[str, Any] = {
            "agentInstanceId": agent_instance_id,
            "settings": settings or {},
        }
        if agent_type:
            payload["agentType"] = agent_type

        self._logger.info(f"Setting settings for agent instance: {agent_instance_id}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.put(
                    endpoint, headers=headers, json=payload
                ) as response:
                    if response.status in (200, 201):
                        data = await self._parse_json_response(response)
                        return AgentSettings(
                            agent_instance_id=data.get(
                                "agentInstanceId", agent_instance_id
                            ),
                            agent_type=data.get("agentType", agent_type),
                            settings=data.get("settings", settings),
                        )
                    else:
                        raise Exception(f"HTTP {response.status}: {await response.text()}")

        except aiohttp.ClientError as http_ex:
            error_msg = (
                f"Failed to set settings for agent instance {agent_instance_id}: {str(http_ex)}"
            )
            self._logger.error(error_msg)
            raise Exception(error_msg) from http_ex

    # --------------------------------------------------------------------------
    # PRIVATE HELPERS
    # --------------------------------------------------------------------------

    def _prepare_headers(self, auth_token: str, options: ToolOptions) -> Dict[str, str]:
        """
        Prepares headers for API requests.

        Args:
            auth_token: Authentication token.
            options: ToolOptions instance containing optional parameters.

        Returns:
            Dictionary of HTTP headers.
        """
        return {
            Constants.Headers.AUTHORIZATION: f"{Constants.Headers.BEARER_PREFIX} {auth_token}",
            Constants.Headers.USER_AGENT: RuntimeUtility.get_user_agent_header(
                options.orchestrator_name
            ),
        }

    async def _parse_json_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """
        Parses JSON response from the API.

        Args:
            response: HTTP response from the API.

        Returns:
            Parsed JSON data as dictionary.
        """
        response_text = await response.text()
        return json.loads(response_text)

    def _validate_agent_type(self, agent_type: str) -> None:
        """
        Validates the agent type parameter.

        Args:
            agent_type: Agent type to validate.

        Raises:
            ValueError: If agent type is invalid or empty.
        """
        if not agent_type or not agent_type.strip():
            raise ValueError("agent_type cannot be empty or None")

    def _validate_agent_instance_id(self, agent_instance_id: str) -> None:
        """
        Validates the agent instance ID parameter.

        Args:
            agent_instance_id: Agent instance ID to validate.

        Raises:
            ValueError: If agent instance ID is invalid or empty.
        """
        if not agent_instance_id or not agent_instance_id.strip():
            raise ValueError("agent_instance_id cannot be empty or None")

    def _validate_auth_token(self, auth_token: str) -> None:
        """
        Validates the authentication token parameter.

        Args:
            auth_token: Authentication token to validate.

        Raises:
            ValueError: If auth token is invalid or empty.
        """
        if not auth_token or not auth_token.strip():
            raise ValueError("auth_token cannot be empty or None")
