# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Utility functions for extracting information from TurnContext.

This module provides helper functions to safely extract common data points
from a TurnContext object, with proper error handling for missing context.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from microsoft_agents.hosting.core.turn_context import TurnContext


def get_tenant_id(turn_context: TurnContext | None) -> str | None:
    """
    Extract the tenant ID from the turn context.

    Args:
        turn_context: The TurnContext containing activity information.

    Returns:
        The tenant ID if available, None otherwise.

    Raises:
        ValueError: If turn_context is None.
    """
    if turn_context is None:
        raise ValueError("turn_context cannot be None")

    if not turn_context.activity:
        return None

    recipient = turn_context.activity.recipient
    if not recipient:
        return None

    return recipient.tenant_id


def get_user_id(turn_context: TurnContext | None) -> str | None:
    """
    Extract the user ID from the turn context.

    Args:
        turn_context: The TurnContext containing activity information.

    Returns:
        The user's AAD object ID if available, None otherwise.

    Raises:
        ValueError: If turn_context is None.
    """
    if turn_context is None:
        raise ValueError("turn_context cannot be None")

    if not turn_context.activity:
        return None

    from_property = turn_context.activity.from_property
    if not from_property:
        return None

    return from_property.aad_object_id


def get_conversation_id(turn_context: TurnContext | None) -> str | None:
    """
    Extract the conversation ID from the turn context.

    Args:
        turn_context: The TurnContext containing activity information.

    Returns:
        The conversation ID if available, None otherwise.

    Raises:
        ValueError: If turn_context is None.
    """
    if turn_context is None:
        raise ValueError("turn_context cannot be None")

    if not turn_context.activity:
        return None

    conversation = turn_context.activity.conversation
    if not conversation:
        return None

    return conversation.id


def get_activity_type(turn_context: TurnContext | None) -> str | None:
    """
    Extract the activity type from the turn context.

    Args:
        turn_context: The TurnContext containing activity information.

    Returns:
        The activity type if available, None otherwise.

    Raises:
        ValueError: If turn_context is None.
    """
    if turn_context is None:
        raise ValueError("turn_context cannot be None")

    if not turn_context.activity:
        return None

    return turn_context.activity.type


def get_channel_id(turn_context: TurnContext | None) -> str | None:
    """
    Extract the channel ID from the turn context.

    Args:
        turn_context: The TurnContext containing activity information.

    Returns:
        The channel ID (as a string or from ChannelId object) if available, None otherwise.

    Raises:
        ValueError: If turn_context is None.
    """
    if turn_context is None:
        raise ValueError("turn_context cannot be None")

    if not turn_context.activity:
        return None

    channel_id = turn_context.activity.channel_id

    if channel_id is None:
        return None

    # Handle both string channel_id and ChannelId object
    # Check for ChannelId object first (which has a .channel attribute)
    if hasattr(channel_id, "channel"):
        return channel_id.channel
    elif isinstance(channel_id, str):
        return channel_id

    return None
