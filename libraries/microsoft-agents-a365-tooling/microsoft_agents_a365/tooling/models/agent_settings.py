# Copyright (c) Microsoft. All rights reserved.

"""
Agent Settings model.

This module provides data models for agent settings, including setting templates
by agent type and settings by agent instance.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class AgentSettingTemplate:
    """
    Represents an agent setting template for a specific agent type.

    Agent setting templates define the default settings configuration for a
    particular type of agent.
    """

    #: The agent type identifier (e.g., "DeclarativeAgent", "EntraEmbodied")
    agent_type: str

    #: The template settings as a dictionary
    settings: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate the template after initialization."""
        if not self.agent_type:
            raise ValueError("agent_type cannot be empty")
        if self.settings is None:
            self.settings = {}


@dataclass
class AgentSettings:
    """
    Represents the settings for a specific agent instance.

    Agent settings are the actual configuration values applied to a particular
    agent instance.
    """

    #: The unique identifier for the agent instance
    agent_instance_id: str

    #: The agent type identifier
    agent_type: Optional[str] = None

    #: The settings for the agent instance as a dictionary
    settings: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate the settings after initialization."""
        if not self.agent_instance_id:
            raise ValueError("agent_instance_id cannot be empty")
        if self.settings is None:
            self.settings = {}
