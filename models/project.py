"""Project model for the Game Dev Studio CLI."""

from datetime import datetime
from typing import List, Optional


class Project:
    """Represents a game project in the studio."""

    def __init__(
        self,
        title: str,
        user_id: str,
        description: str = "",
        project_id: Optional[str] = None,
        created_at: Optional[str] = None,
        tasks: Optional[List[str]] = None,
    ):
        """Initialize a Project.

        Args:
            title: Title of the game/project
            user_id: ID of the project owner/lead
            description: Project description
            project_id: Unique identifier (auto-generated if None)
            created_at: Creation timestamp (auto-generated if None)
            tasks: List of task IDs (default: empty)
        """
        self.project_id = project_id or self._generate_id()
        self.title = title
        self.user_id = user_id
        self.description = description
        self.created_at = created_at or datetime.now().isoformat()
        self.tasks = tasks or []

    @staticmethod
    def _generate_id() -> str:
        """Generate a unique project ID."""
        from datetime import datetime

        return f"project_{datetime.now().timestamp()}"

    def add_task(self, task_id: str) -> None:
        """Add a task to the project.

        Args:
            task_id: ID of the task to add
        """
        if task_id not in self.tasks:
            self.tasks.append(task_id)

    def remove_task(self, task_id: str) -> bool:
        """Remove a task from the project.

        Args:
            task_id: ID of the task to remove

        Returns:
            True if task was removed, False if not found
        """
        if task_id in self.tasks:
            self.tasks.remove(task_id)
            return True
        return False

    def get_task_count(self) -> int:
        """Get the number of tasks in this project."""
        return len(self.tasks)

    def to_dict(self) -> dict:
        """Convert project to dictionary representation."""
        return {
            "project_id": self.project_id,
            "title": self.title,
            "user_id": self.user_id,
            "description": self.description,
            "created_at": self.created_at,
            "tasks": self.tasks,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        """Create Project from dictionary representation."""
        return cls(
            title=data["title"],
            user_id=data["user_id"],
            description=data.get("description", ""),
            project_id=data.get("project_id"),
            created_at=data.get("created_at"),
            tasks=data.get("tasks", []),
        )

    def __repr__(self) -> str:
        return f"Project({self.project_id}: {self.title} - {len(self.tasks)} tasks)"
