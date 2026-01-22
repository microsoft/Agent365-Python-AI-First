# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Unit tests for turn_context_utils module.
"""

from unittest.mock import MagicMock

import pytest
from microsoft_agents.activity import Activity, ChannelAccount, ChannelId, ConversationAccount
from microsoft_agents.hosting.core.turn_context import TurnContext

from microsoft_agents_a365.observability.hosting.utils.turn_context_utils import (
    get_activity_type,
    get_channel_id,
    get_conversation_id,
    get_tenant_id,
    get_user_id,
)


def test_get_tenant_id_with_valid_context():
    """Test get_tenant_id extracts tenant ID from turn context with valid data."""
    recipient = ChannelAccount(tenant_id="test-tenant-123")
    activity = Activity(type="message", recipient=recipient)
    adapter = MagicMock()
    turn_context = TurnContext(adapter, activity)

    result = get_tenant_id(turn_context)

    assert result == "test-tenant-123"


def test_get_tenant_id_with_none_context():
    """Test get_tenant_id raises ValueError when turn_context is None."""
    with pytest.raises(ValueError, match="turn_context cannot be None"):
        get_tenant_id(None)


def test_get_tenant_id_with_no_activity():
    """Test get_tenant_id returns None when activity is missing."""
    adapter = MagicMock()
    turn_context = MagicMock()
    turn_context.activity = None

    result = get_tenant_id(turn_context)

    assert result is None


def test_get_tenant_id_with_no_recipient():
    """Test get_tenant_id returns None when recipient is missing."""
    # Create activity without recipient by not setting it - use only required fields
    activity = Activity(type="message")
    adapter = MagicMock()
    turn_context = TurnContext(adapter, activity)

    result = get_tenant_id(turn_context)

    assert result is None


def test_get_user_id_with_valid_context():
    """Test get_user_id extracts user AAD object ID from turn context."""
    from_account = ChannelAccount(aad_object_id="user-aad-456")
    activity = Activity(type="message", from_property=from_account)
    adapter = MagicMock()
    turn_context = TurnContext(adapter, activity)

    result = get_user_id(turn_context)

    assert result == "user-aad-456"


def test_get_user_id_with_none_context():
    """Test get_user_id raises ValueError when turn_context is None."""
    with pytest.raises(ValueError, match="turn_context cannot be None"):
        get_user_id(None)


def test_get_user_id_with_no_activity():
    """Test get_user_id returns None when activity is missing."""
    turn_context = MagicMock()
    turn_context.activity = None

    result = get_user_id(turn_context)

    assert result is None


def test_get_user_id_with_no_from_property():
    """Test get_user_id returns None when from_property is missing."""
    activity = Activity(type="message")
    adapter = MagicMock()
    turn_context = TurnContext(adapter, activity)

    result = get_user_id(turn_context)

    assert result is None


def test_get_conversation_id_with_valid_context():
    """Test get_conversation_id extracts conversation ID from turn context."""
    conversation = ConversationAccount(id="conv-789")
    activity = Activity(type="message", conversation=conversation)
    adapter = MagicMock()
    turn_context = TurnContext(adapter, activity)

    result = get_conversation_id(turn_context)

    assert result == "conv-789"


def test_get_conversation_id_with_none_context():
    """Test get_conversation_id raises ValueError when turn_context is None."""
    with pytest.raises(ValueError, match="turn_context cannot be None"):
        get_conversation_id(None)


def test_get_conversation_id_with_no_activity():
    """Test get_conversation_id returns None when activity is missing."""
    turn_context = MagicMock()
    turn_context.activity = None

    result = get_conversation_id(turn_context)

    assert result is None


def test_get_conversation_id_with_no_conversation():
    """Test get_conversation_id returns None when conversation is missing."""
    activity = Activity(type="message")
    adapter = MagicMock()
    turn_context = TurnContext(adapter, activity)

    result = get_conversation_id(turn_context)

    assert result is None


def test_get_activity_type_with_valid_context():
    """Test get_activity_type extracts activity type from turn context."""
    activity = Activity(type="messageReaction")
    adapter = MagicMock()
    turn_context = TurnContext(adapter, activity)

    result = get_activity_type(turn_context)

    assert result == "messageReaction"


def test_get_activity_type_with_none_context():
    """Test get_activity_type raises ValueError when turn_context is None."""
    with pytest.raises(ValueError, match="turn_context cannot be None"):
        get_activity_type(None)


def test_get_activity_type_with_no_activity():
    """Test get_activity_type returns None when activity is missing."""
    turn_context = MagicMock()
    turn_context.activity = None

    result = get_activity_type(turn_context)

    assert result is None


def test_get_channel_id_with_string_channel():
    """Test get_channel_id extracts channel ID when it's a string."""
    activity = Activity(type="message", channel_id="msteams")
    adapter = MagicMock()
    turn_context = TurnContext(adapter, activity)

    result = get_channel_id(turn_context)

    assert result == "msteams"


def test_get_channel_id_with_channel_object():
    """Test get_channel_id extracts channel ID when it's a ChannelId object."""
    channel_obj = ChannelId(channel="msteams", sub_channel="general")
    activity = Activity(type="message", channel_id=channel_obj)
    adapter = MagicMock()
    turn_context = TurnContext(adapter, activity)

    result = get_channel_id(turn_context)

    assert result == "msteams"


def test_get_channel_id_with_none_context():
    """Test get_channel_id raises ValueError when turn_context is None."""
    with pytest.raises(ValueError, match="turn_context cannot be None"):
        get_channel_id(None)


def test_get_channel_id_with_no_activity():
    """Test get_channel_id returns None when activity is missing."""
    turn_context = MagicMock()
    turn_context.activity = None

    result = get_channel_id(turn_context)

    assert result is None


def test_get_channel_id_with_no_channel_id():
    """Test get_channel_id returns None when channel_id is missing."""
    activity = Activity(type="message")
    adapter = MagicMock()
    turn_context = TurnContext(adapter, activity)

    result = get_channel_id(turn_context)

    assert result is None


def test_all_functions_with_complete_context():
    """Test all utility functions work together with a complete context."""
    from_account = ChannelAccount(aad_object_id="user-123")
    recipient = ChannelAccount(tenant_id="tenant-456")
    conversation = ConversationAccount(id="conv-789")
    activity = Activity(
        type="message",
        from_property=from_account,
        recipient=recipient,
        conversation=conversation,
        channel_id="webchat",
    )
    adapter = MagicMock()
    turn_context = TurnContext(adapter, activity)

    assert get_tenant_id(turn_context) == "tenant-456"
    assert get_user_id(turn_context) == "user-123"
    assert get_conversation_id(turn_context) == "conv-789"
    assert get_activity_type(turn_context) == "message"
    assert get_channel_id(turn_context) == "webchat"
