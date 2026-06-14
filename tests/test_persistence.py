"""Tests for data persistence."""

import pytest
import json
import tempfile
import os
from models import User, Project, Task
from utils import StudioDataManager


@pytest.fixture
def temp_data_file():
    """Create a temporary data file for testing."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


class TestStudioDataManager:
    """Test StudioDataManager functionality."""

    def test_initialization(self, temp_data_file):
        """Test manager initialization."""
        manager = StudioDataManager(temp_data_file)
        assert os.path.exists(temp_data_file)
        assert len(manager.users) == 0
        assert len(manager.projects) == 0
        assert len(manager.tasks) == 0

    def test_add_user(self, temp_data_file):
        """Test adding a user."""
        manager = StudioDataManager(temp_data_file)
        user = User(name="Test User")
        assert manager.add_user(user) is True
        assert len(manager.users) == 1
        assert manager.get_user(user.user_id) == user

    def test_duplicate_user(self, temp_data_file):
        """Test that duplicate users cannot be added."""
        manager = StudioDataManager(temp_data_file)
        user = User(name="Duplicate", user_id="user_1")
        assert manager.add_user(user) is True
        assert manager.add_user(user) is False

    def test_get_user_by_name(self, temp_data_file):
        """Test retrieving user by name."""
        manager = StudioDataManager(temp_data_file)
        user = User(name="FindMe")
        manager.add_user(user)
        found = manager.get_user_by_name("FindMe")
        assert found is not None
        assert found.name == "FindMe"

    def test_list_users(self, temp_data_file):
        """Test listing all users."""
        manager = StudioDataManager(temp_data_file)
        user1 = User(name="User1")
        user2 = User(name="User2")
        manager.add_user(user1)
        manager.add_user(user2)
        users = manager.list_users()
        assert len(users) == 2

    def test_delete_user(self, temp_data_file):
        """Test deleting a user."""
        manager = StudioDataManager(temp_data_file)
        user = User(name="ToDelete")
        manager.add_user(user)
        assert manager.delete_user(user.user_id) is True
        assert len(manager.users) == 0

    def test_add_project(self, temp_data_file):
        """Test adding a project."""
        manager = StudioDataManager(temp_data_file)
        user = User(name="Lead")
        manager.add_user(user)
        project = Project(title="Game", user_id=user.user_id)
        assert manager.add_project(project) is True
        assert len(manager.projects) == 1

    def test_get_project_by_title(self, temp_data_file):
        """Test retrieving project by title."""
        manager = StudioDataManager(temp_data_file)
        user = User(name="Dev")
        manager.add_user(user)
        project = Project(title="MyGame", user_id=user.user_id)
        manager.add_project(project)
        found = manager.get_project_by_title("MyGame")
        assert found is not None
        assert found.title == "MyGame"

    def test_list_user_projects(self, temp_data_file):
        """Test listing projects for a specific user."""
        manager = StudioDataManager(temp_data_file)
        user = User(name="Developer")
        manager.add_user(user)
        proj1 = Project(title="Game1", user_id=user.user_id)
        proj2 = Project(title="Game2", user_id=user.user_id)
        manager.add_project(proj1)
        manager.add_project(proj2)
        projects = manager.list_user_projects(user.user_id)
        assert len(projects) == 2

    def test_add_task(self, temp_data_file):
        """Test adding a task."""
        manager = StudioDataManager(temp_data_file)
        user = User(name="Coder")
        manager.add_user(user)
        project = Project(title="Project", user_id=user.user_id)
        manager.add_project(project)
        task = Task(title="Feature", project_id=project.project_id)
        assert manager.add_task(task) is True
        assert len(manager.tasks) == 1

    def test_list_project_tasks(self, temp_data_file):
        """Test listing tasks for a project."""
        manager = StudioDataManager(temp_data_file)
        user = User(name="Programmer")
        manager.add_user(user)
        project = Project(title="GameProject", user_id=user.user_id)
        manager.add_project(project)
        task1 = Task(title="Task1", project_id=project.project_id)
        task2 = Task(title="Task2", project_id=project.project_id)
        manager.add_task(task1)
        manager.add_task(task2)
        tasks = manager.list_project_tasks(project.project_id)
        assert len(tasks) == 2

    def test_update_task(self, temp_data_file):
        """Test updating a task."""
        manager = StudioDataManager(temp_data_file)
        user = User(name="Worker")
        manager.add_user(user)
        project = Project(title="Work", user_id=user.user_id)
        manager.add_project(project)
        task = Task(title="Todo", project_id=project.project_id)
        manager.add_task(task)
        assert manager.update_task(task.task_id, status="in-progress") is True
        updated = manager.get_task(task.task_id)
        assert updated.status == "in-progress"

    def test_persistence(self, temp_data_file):
        """Test that data persists between manager instances."""
        # Create and populate manager
        manager1 = StudioDataManager(temp_data_file)
        user = User(name="Persist")
        manager1.add_user(user)
        user_id = user.user_id

        # Create new manager and check if user still exists
        manager2 = StudioDataManager(temp_data_file)
        found = manager2.get_user(user_id)
        assert found is not None
        assert found.name == "Persist"
