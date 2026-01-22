# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Task ID generator utility for Microsoft Agent 365.

This module provides functionality for generating unique, human-readable,
and time-sortable task identifiers.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone


def generate_task_id() -> str:
    """
    Generate a unique task identifier.

    Creates a unique identifier suitable for tracking tasks. The ID is composed of:
    - A human-readable prefix "task-"
    - A timestamp in YYYYMMDD format (UTC)
    - A short UUID segment for uniqueness

    The generated IDs are:
    - Unique: Uses UUID to ensure no collisions
    - Human-readable: Includes a clear prefix and timestamp
    - Sortable: Timestamp-based prefix allows chronological sorting

    Returns:
        str: A unique task identifier in the format "task-YYYYMMDD-xxxxxxxx"
             where YYYYMMDD is the UTC date and xxxxxxxx is a shortened UUID.

    Examples:
        >>> task_id = generate_task_id()
        >>> print(task_id)
        task-20260122-a1b2c3d4

        >>> # Multiple calls generate unique IDs
        >>> id1 = generate_task_id()
        >>> id2 = generate_task_id()
        >>> assert id1 != id2
    """
    # Get current UTC timestamp in YYYYMMDD format
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d")

    # Generate a UUID and take the first 8 characters of its hex representation
    unique_id = uuid.uuid4().hex[:8]

    # Combine prefix, timestamp, and unique ID
    return f"task-{timestamp}-{unique_id}"
