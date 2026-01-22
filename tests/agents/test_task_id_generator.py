# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Unit tests for task_id_generator module."""

import re
from datetime import datetime, timezone

import pytest
from agents.utils.task_id_generator import generate_task_id


def test_generate_task_id_returns_string():
    """Test that generate_task_id returns a string."""
    task_id = generate_task_id()
    assert isinstance(task_id, str)


def test_generate_task_id_has_correct_prefix():
    """Test that generated task IDs have the 'task-' prefix."""
    task_id = generate_task_id()
    assert task_id.startswith("task-")


def test_generate_task_id_format():
    """Test that generated task IDs match the expected format."""
    task_id = generate_task_id()
    # Expected format: task-YYYYMMDD-xxxxxxxx
    # where YYYYMMDD is a date and xxxxxxxx is an 8-character hex string
    pattern = r"^task-\d{8}-[0-9a-f]{8}$"
    assert re.match(pattern, task_id), f"Task ID '{task_id}' does not match expected format"


def test_generate_task_id_contains_current_date():
    """Test that generated task IDs contain the current UTC date."""
    current_date = datetime.now(timezone.utc).strftime("%Y%m%d")
    task_id = generate_task_id()
    assert current_date in task_id


def test_generate_task_id_uniqueness():
    """Test that multiple calls generate unique task IDs."""
    # Generate multiple IDs
    task_ids = [generate_task_id() for _ in range(100)]

    # Check that all IDs are unique
    assert len(task_ids) == len(set(task_ids)), "Generated task IDs are not unique"


def test_generate_task_id_sortability():
    """Test that task IDs are sortable by creation time."""
    # Capture current date before generating IDs to avoid race conditions
    current_date = datetime.now(timezone.utc).strftime("%Y%m%d")
    
    # Generate a list of task IDs
    task_ids = [generate_task_id() for _ in range(10)]

    # Since all are generated in rapid succession on the same date,
    # they should all have the same date prefix
    dates = [task_id.split("-")[1] for task_id in task_ids]
    assert all(d == dates[0] for d in dates), "Task IDs have inconsistent date prefixes"

    # Verify the format allows for sorting (date is in YYYYMMDD format)
    # This ensures future dates will sort after current dates
    assert all(d == current_date for d in dates)


def test_generate_task_id_no_parameters():
    """Test that generate_task_id can be called with no parameters."""
    # Should not raise any exceptions
    task_id = generate_task_id()
    assert task_id is not None
    assert len(task_id) > 0
