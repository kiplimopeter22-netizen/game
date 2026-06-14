"""Tests for Task model."""

import pytest
from models import Task


class TestTaskInitialization:
    """Test Task initialization."""

    def test_task_creation_with_defaults(self):
        """Test creating a task with default values."""
        task = Task(title="Create menu", project_id="proj_1")
        assert task.title == "Create menu"
        assert task.project_id == "proj_1"
        assert task.status == "backlog"
        assert task.assigned_to is None

    def test_task_creation_with_all_fields(self):
        """Test creating a task with all fields specified."""
        task = Task(
            title="Fix bug",
            project_id="proj_1",
            status="in-progress",
            assigned_to="user_1",
            task_id="task_123",
        )
        assert task.title == "Fix bug"
        assert task.status == "in-progress"
        assert task.assigned_to == "user_1"
        assert task.task_id == "task_123"

    def test_invalid_status_defaults_to_backlog(self):
        """Test that invalid statuses default to backlog."""
        task = Task(title="Test", project_id="proj_1", status="invalid_status")
        assert task.status == "backlog"


class TestTaskMethods:
    """Test Task methods."""

    def test_update_status_valid(self):
        """Test updating task status to a valid status."""
        task = Task(title="Feature", project_id="proj_1")
        assert task.update_status("in-progress") is True
        assert task.status == "in-progress"

    def test_update_status_invalid(self):
        """Test updating task status to an invalid status."""
        task = Task(title="Feature", project_id="proj_1")
        assert task.update_status("invalid") is False
        assert task.status == "backlog"

    def test_update_status_sequence(self):
        """Test the valid status sequence."""
        task = Task(title="Feature", project_id="proj_1")
        assert task.update_status("in-progress") is True
        assert task.update_status("playtesting") is True
        assert task.update_status("shipped") is True

    def test_assign_to_user(self):
        """Test assigning a task to a user."""
        task = Task(title="Implementation", project_id="proj_1")
        task.assign_to("user_2")
        assert task.assigned_to == "user_2"


class TestTaskSerialization:
    """Test Task serialization."""

    def test_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(
            title="Graphics",
            project_id="proj_1",
            status="in-progress",
            assigned_to="user_3",
        )
        task_dict = task.to_dict()
        assert task_dict["title"] == "Graphics"
        assert task_dict["project_id"] == "proj_1"
        assert task_dict["status"] == "in-progress"
        assert task_dict["assigned_to"] == "user_3"

    def test_from_dict(self):
        """Test creating task from dictionary."""
        data = {
            "title": "Sound Design",
            "project_id": "proj_1",
            "status": "playtesting",
            "assigned_to": "user_4",
            "task_id": "task_789",
        }
        task = Task.from_dict(data)
        assert task.title == "Sound Design"
        assert task.status == "playtesting"
        assert task.assigned_to == "user_4"
        assert task.task_id == "task_789"
