# Copyright (c) Microsoft. All rights reserved.

from enum import Enum


class InferenceOperationType(Enum):
    """Supported inference operation types for generative AI."""

    CHAT = "Chat"
    TEXT_COMPLETION = "TextCompletion"
    GENERATE_CONTENT = "GenerateContent"
