# Copyright (c) Microsoft. All rights reserved.

# Tool type enum.

from enum import Enum


class ToolType(Enum):
    """Enumeration for different tool types for execute tool contexts."""

    FUNCTION = "function"
    EXTENSION = "extension"
    DATASTORE = "datastore"
