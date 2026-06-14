"""Tests for Project model."""

import pytest
from models import Project


class TestProjectInitialization:
    """Test Project initialization."""

    def test_project_creation_with_defaults(self):
        """Test creating a project with default values."""
        project = Project(title="Awesome Game", user_id="user_1")
        assert project.title == "Awesome Game"
        assert project.user_id == "user_1"
        assert project.description == ""
        assert project.tasks == []

    def test_project_creation_with_all_fields(self):
        """Test creating a project with all fields specified."""
        project = Project(
            title="Epic Quest",
            user_id="user_2",
            description="An epic RPG adventure",
            project_id="proj_123",
            tasks=["task_1", "task_2"],
        )
        assert project.title == "Epic Quest"
        assert project.description == "An epic RPG adventure"
        assert len(project.tasks) == 2


class TestProjectMethods:
    """Test Project methods."""

    def test_add_task(self):
        """Test adding a task to a project."""
        project = Project(title="Game A", user_id="user_1")
        project.add_task("task_1")
        assert "task_1" in project.tasks
        assert project.get_task_count() == 1

    def test_add_duplicate_task(self):
        """Test that duplicate tasks are not added twice."""
        project = Project(title="Game B", user_id="user_1")
        project.add_task("task_1")
        project.add_task("task_1")
        assert project.get_task_count() == 1

    def test_remove_task(self):
        """Test removing a task from a project."""
        project = Project(title="Game C", user_id="user_1", tasks=["task_1", "task_2"])
        assert project.remove_task("task_1") is True
        assert "task_1" not in project.tasks
        assert project.get_task_count() == 1

    def test_remove_nonexistent_task(self):
        """Test removing a task that doesn't exist."""
        project = Project(title="Game D", user_id="user_1")
        assert project.remove_task("task_1") is False


class TestProjectSerialization:
    """Test Project serialization."""

    def test_to_dict(self):
        """Test converting project to dictionary."""
        project = Project(
            title="Strategy Game",
            user_id="user_3",
            description="A turn-based strategy game",
        )
        project_dict = project.to_dict()
        assert project_dict["title"] == "Strategy Game"
        assert project_dict["user_id"] == "user_3"
        assert project_dict["description"] == "A turn-based strategy game"

    def test_from_dict(self):
        """Test creating project from dictionary."""
        data = {
            "title": "Puzzle Game",
            "user_id": "user_4",
            "description": "A challenging puzzle game",
            "project_id": "proj_456",
            "tasks": ["task_1", "task_2", "task_3"],
        }
        project = Project.from_dict(data)
        assert project.title == "Puzzle Game"
        assert project.user_id == "user_4"
        assert project.project_id == "proj_456"
        assert len(project.tasks) == 3
