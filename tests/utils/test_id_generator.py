# Copyright (c) Microsoft. All rights reserved.

"""Unit tests for ID generator utility."""

import re
import uuid
from datetime import datetime

import pytest

from agents.utils.id_generator import generate_task_id


class TestGenerateTaskId:
    """Tests for generate_task_id function."""

    def test_generate_task_id_default_prefix(self):
        """Test task ID generation with default prefix."""
        task_id = generate_task_id()

        # Check the format: prefix_timestamp_uuid
        parts = task_id.split("_")
        assert parts[0] == "task", "Default prefix should be 'task'"
        assert len(parts) >= 3, "Task ID should have at least 3 parts"

        # Verify timestamp is numeric
        assert parts[1].isdigit(), "Timestamp should be numeric"

        # Verify UUID part is valid
        uuid_part = "_".join(parts[2:])
        try:
            uuid.UUID(uuid_part)
        except ValueError:
            pytest.fail(f"UUID part '{uuid_part}' is not a valid UUID")

    def test_generate_task_id_custom_prefix(self):
        """Test task ID generation with custom prefix."""
        custom_prefix = "custom"
        task_id = generate_task_id(prefix=custom_prefix)

        assert task_id.startswith(f"{custom_prefix}_"), f"Task ID should start with '{custom_prefix}_'"

    def test_generate_task_id_uniqueness(self):
        """Test that generated IDs are unique."""
        task_ids = [generate_task_id() for _ in range(100)]

        # All IDs should be unique
        assert len(task_ids) == len(set(task_ids)), "All generated task IDs should be unique"

    def test_generate_task_id_format(self):
        """Test that generated ID matches expected format."""
        task_id = generate_task_id(prefix="test")

        # Format: prefix_timestamp_uuid
        # UUID format: 8-4-4-4-12 hex digits
        pattern = r"^test_\d+_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
        assert re.match(pattern, task_id), f"Task ID '{task_id}' does not match expected format"

    def test_generate_task_id_empty_prefix(self):
        """Test task ID generation with empty prefix."""
        task_id = generate_task_id(prefix="")

        # Even with empty prefix, should have _timestamp_uuid format
        assert task_id.startswith("_"), "Task ID with empty prefix should start with '_'"

    def test_generate_task_id_timestamp_recent(self):
        """Test that timestamp in generated ID is recent."""
        before_timestamp = int(datetime.now().timestamp())
        task_id = generate_task_id()
        after_timestamp = int(datetime.now().timestamp())

        # Extract timestamp from task ID
        parts = task_id.split("_")
        id_timestamp = int(parts[1])

        # Timestamp should be between before and after
        assert before_timestamp <= id_timestamp <= after_timestamp, \
            "Timestamp should be within the time of generation"
