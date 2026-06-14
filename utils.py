"""Data persistence layer for Game Dev Studio CLI."""

import json
import os
from typing import Dict, List, Optional, Tuple
from models import User, Project, Task


class StudioDataManager:
    """Manages persistence of studio data to JSON."""

    def __init__(self, data_file: str = "data/studio.json"):
        """Initialize the data manager.

        Args:
            data_file: Path to the JSON data file
        """
        self.data_file = data_file
        self.users: Dict[str, User] = {}
        self.projects: Dict[str, Project] = {}
        self.tasks: Dict[str, Task] = {}
        self._ensure_data_file()
        self.load_data()

    def _ensure_data_file(self) -> None:
        """Ensure the data directory and file exist."""
        dir_path = os.path.dirname(self.data_file)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Initialize with empty structure if file doesn't exist or is empty
        if not os.path.exists(self.data_file) or os.path.getsize(self.data_file) == 0:
            initial_data = {
                "users": {},
                "projects": {},
                "tasks": {},
            }
            with open(self.data_file, "w") as f:
                json.dump(initial_data, f, indent=2)

    def load_data(self) -> None:
        """Load all data from JSON file."""
        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)

            # Load users
            for user_id, user_data in data.get("users", {}).items():
                self.users[user_id] = User.from_dict(user_data)

            # Load projects
            for project_id, project_data in data.get("projects", {}).items():
                self.projects[project_id] = Project.from_dict(project_data)

            # Load tasks
            for task_id, task_data in data.get("tasks", {}).items():
                self.tasks[task_id] = Task.from_dict(task_data)

        except Exception as e:
            raise RuntimeError(f"Failed to load data from {self.data_file}: {e}")

    def save_data(self) -> None:
        """Save all data to JSON file."""
        try:
            data = {
                "users": {uid: user.to_dict() for uid, user in self.users.items()},
                "projects": {
                    pid: project.to_dict() for pid, project in self.projects.items()
                },
                "tasks": {tid: task.to_dict() for tid, task in self.tasks.items()},
            }

            with open(self.data_file, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            raise RuntimeError(f"Failed to save data to {self.data_file}: {e}")

    # User operations
    def add_user(self, user: User) -> bool:
        """Add a user to the studio.

        Args:
            user: User object to add

        Returns:
            True if added successfully, False if user already exists
        """
        if user.user_id in self.users:
            return False
        self.users[user.user_id] = user
        self.save_data()
        return True

    def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID.

        Args:
            user_id: ID of the user to retrieve

        Returns:
            User object or None if not found
        """
        return self.users.get(user_id)

    def get_user_by_name(self, name: str) -> Optional[User]:
        """Get a user by name.

        Args:
            name: Name of the user to retrieve

        Returns:
            User object or None if not found
        """
        for user in self.users.values():
            if user.name.lower() == name.lower():
                return user
        return None

    def list_users(self) -> List[User]:
        """Get all users."""
        return list(self.users.values())

    def delete_user(self, user_id: str) -> bool:
        """Delete a user from the studio.

        Args:
            user_id: ID of the user to delete

        Returns:
            True if deleted successfully, False if not found
        """
        if user_id in self.users:
            user = self.users[user_id]
            # Remove user from all projects
            for project_id in user.projects:
                if project_id in self.projects:
                    self.projects[project_id].remove_task(user_id)
            del self.users[user_id]
            self.save_data()
            return True
        return False

    # Project operations
    def add_project(self, project: Project) -> bool:
        """Add a project to the studio.

        Args:
            project: Project object to add

        Returns:
            True if added successfully, False if project already exists
        """
        if project.project_id in self.projects:
            return False
        self.projects[project.project_id] = project
        # Add to user's project list
        if project.user_id in self.users:
            self.users[project.user_id].add_project(project.project_id)
        self.save_data()
        return True

    def get_project(self, project_id: str) -> Optional[Project]:
        """Get a project by ID.

        Args:
            project_id: ID of the project to retrieve

        Returns:
            Project object or None if not found
        """
        return self.projects.get(project_id)

    def get_project_by_title(self, title: str) -> Optional[Project]:
        """Get a project by title.

        Args:
            title: Title of the project to retrieve

        Returns:
            Project object or None if not found
        """
        for project in self.projects.values():
            if project.title.lower() == title.lower():
                return project
        return None

    def list_projects(self) -> List[Project]:
        """Get all projects."""
        return list(self.projects.values())

    def list_user_projects(self, user_id: str) -> List[Project]:
        """Get all projects for a specific user.

        Args:
            user_id: ID of the user

        Returns:
            List of projects owned by the user
        """
        user = self.get_user(user_id)
        if not user:
            return []
        return [self.projects[pid] for pid in user.projects if pid in self.projects]

    def delete_project(self, project_id: str) -> bool:
        """Delete a project from the studio.

        Args:
            project_id: ID of the project to delete

        Returns:
            True if deleted successfully, False if not found
        """
        if project_id in self.projects:
            project = self.projects[project_id]
            # Remove from user's project list
            if project.user_id in self.users:
                self.users[project.user_id].remove_project(project_id)
            # Delete all tasks in the project
            for task_id in project.tasks:
                if task_id in self.tasks:
                    del self.tasks[task_id]
            del self.projects[project_id]
            self.save_data()
            return True
        return False

    # Task operations
    def add_task(self, task: Task) -> bool:
        """Add a task to the studio.

        Args:
            task: Task object to add

        Returns:
            True if added successfully, False if task already exists
        """
        if task.task_id in self.tasks:
            return False
        self.tasks[task.task_id] = task
        # Add to project's task list
        if task.project_id in self.projects:
            self.projects[task.project_id].add_task(task.task_id)
        self.save_data()
        return True

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task object or None if not found
        """
        return self.tasks.get(task_id)

    def list_tasks(self) -> List[Task]:
        """Get all tasks."""
        return list(self.tasks.values())

    def list_project_tasks(self, project_id: str) -> List[Task]:
        """Get all tasks for a specific project.

        Args:
            project_id: ID of the project

        Returns:
            List of tasks in the project
        """
        project = self.get_project(project_id)
        if not project:
            return []
        return [self.tasks[tid] for tid in project.tasks if tid in self.tasks]

    def delete_task(self, task_id: str) -> bool:
        """Delete a task from the studio.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if deleted successfully, False if not found
        """
        if task_id in self.tasks:
            task = self.tasks[task_id]
            # Remove from project's task list
            if task.project_id in self.projects:
                self.projects[task.project_id].remove_task(task_id)
            del self.tasks[task_id]
            self.save_data()
            return True
        return False

    def update_task(self, task_id: str, **kwargs) -> bool:
        """Update task properties.

        Args:
            task_id: ID of the task to update
            **kwargs: Properties to update (status, assigned_to, title)

        Returns:
            True if updated successfully, False if task not found
        """
        task = self.get_task(task_id)
        if not task:
            return False

        if "status" in kwargs:
            task.update_status(kwargs["status"])
        if "assigned_to" in kwargs:
            task.assign_to(kwargs["assigned_to"])
        if "title" in kwargs:
            task.title = kwargs["title"]

        self.save_data()
        return True
