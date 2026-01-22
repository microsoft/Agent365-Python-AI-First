# Copyright (c) Microsoft. All rights reserved.

"""Utility module for generating unique identifiers."""

import uuid
from datetime import datetime


def generate_task_id(prefix: str = "task") -> str:
    """
    Generate a unique task identifier.

    Args:
        prefix: Optional prefix for the task ID (default: "task")

    Returns:
        A unique task identifier string in format: {prefix}_{timestamp}_{uuid}
    """
    timestamp = int(datetime.now().timestamp())
    unique_id = str(uuid.uuid4())
    return f"{prefix}_{timestamp}_{unique_id}"
