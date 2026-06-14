"""Task model for the Game Dev Studio CLI."""

from datetime import datetime
from typing import Optional


class Task:
    """Represents a game feature/task in the studio."""

    # Valid status transitions: backlog → in-progress → playtesting → shipped
    VALID_STATUSES = ["backlog", "in-progress", "playtesting", "shipped"]

    def __init__(
        self,
        title: str,
        project_id: str,
        status: str = "backlog",
        assigned_to: Optional[str] = None,
        task_id: Optional[str] = None,
        created_at: Optional[str] = None,
    ):
        """Initialize a Task.

        Args:
            title: Title of the task/feature
            project_id: ID of the project this task belongs to
            status: Current status (default: backlog)
            assigned_to: User ID of assigned developer
            task_id: Unique identifier (auto-generated if None)
            created_at: Creation timestamp (auto-generated if None)
        """
        self.task_id = task_id or self._generate_id()
        self.title = title
        self.project_id = project_id
        self.status = status if status in self.VALID_STATUSES else "backlog"
        self.assigned_to = assigned_to
        self.created_at = created_at or datetime.now().isoformat()

    @staticmethod
    def _generate_id() -> str:
        """Generate a unique task ID."""
        from datetime import datetime

        return f"task_{datetime.now().timestamp()}"

    def update_status(self, new_status: str) -> bool:
        """Update task status if valid.

        Args:
            new_status: New status to set

        Returns:
            True if status was updated, False otherwise
        """
        if new_status in self.VALID_STATUSES:
            self.status = new_status
            return True
        return False

    def assign_to(self, user_id: str) -> None:
        """Assign task to a user.

        Args:
            user_id: ID of the user to assign to
        """
        self.assigned_to = user_id

    def to_dict(self) -> dict:
        """Convert task to dictionary representation."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "project_id": self.project_id,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create Task from dictionary representation."""
        return cls(
            title=data["title"],
            project_id=data["project_id"],
            status=data.get("status", "backlog"),
            assigned_to=data.get("assigned_to"),
            task_id=data.get("task_id"),
            created_at=data.get("created_at"),
        )

    def __repr__(self) -> str:
        return f"Task({self.task_id}: {self.title} [{self.status}])"
