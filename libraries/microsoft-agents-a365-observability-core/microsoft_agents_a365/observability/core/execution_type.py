# Copyright (c) Microsoft. All rights reserved.

# Execution type enum.

from enum import Enum


class ExecutionType(Enum):
    """Enumeration for different types of agent execution contexts."""

    AGENT_TO_AGENT = "Agent2Agent"
    EVENT_TO_AGENT = "EventToAgent"
    HUMAN_TO_AGENT = "HumanToAgent"
