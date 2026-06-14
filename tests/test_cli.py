"""Tests for CLI commands."""

import pytest
from unittest.mock import MagicMock
import tempfile
import os
from models import User, Project, Task
from utils import StudioDataManager
from cli.commands import (
    cmd_add_user,
    cmd_add_project,
    cmd_add_task,
    cmd_update_status,
)


@pytest.fixture
def temp_data_file():
    """Create a temporary data file for testing."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def manager(temp_data_file):
    """Create a test manager."""
    return StudioDataManager(temp_data_file)


class TestCLICommands:
    """Test CLI command functions."""

    def test_cmd_add_user(self, manager):
        """Test add-user command."""
        args = MagicMock()
        args.name = "Alice"
        args.role = "lead"
        args.email = "alice@studio.com"
        cmd_add_user(args, manager)
        users = manager.list_users()
        assert len(users) == 1
        assert users[0].name == "Alice"

    def test_cmd_add_project(self, manager):
        """Test add-project command."""
        # First add a user
        user = User(name="Bob", role="senior")
        manager.add_user(user)

        # Now add project
        args = MagicMock()
        args.user = "Bob"
        args.title = "Space Game"
        args.description = "An exciting space adventure"
        cmd_add_project(args, manager)

        projects = manager.list_projects()
        assert len(projects) == 1
        assert projects[0].title == "Space Game"

    def test_cmd_add_task(self, manager):
        """Test add-task command."""
        # Setup user and project
        user = User(name="Charlie")
        manager.add_user(user)
        project = Project(title="RPG", user_id=user.user_id)
        manager.add_project(project)

        # Add task
        args = MagicMock()
        args.project = "RPG"
        args.title = "Create character system"
        cmd_add_task(args, manager)

        tasks = manager.list_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Create character system"

    def test_cmd_update_status(self, manager):
        """Test update-status command."""
        # Setup
        user = User(name="Dave")
        manager.add_user(user)
        project = Project(title="Adventure", user_id=user.user_id)
        manager.add_project(project)
        task = Task(title="Main quest", project_id=project.project_id)
        manager.add_task(task)

        # Update status
        args = MagicMock()
        args.task = "Main quest"
        args.status = "in-progress"
        cmd_update_status(args, manager)

        updated = manager.get_task(task.task_id)
        assert updated.status == "in-progress"
