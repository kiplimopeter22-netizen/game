"""User model for the Game Dev Studio CLI."""

from datetime import datetime
from typing import List, Optional


class User:
    """Represents a developer role in the studio."""

    # Valid developer roles
    VALID_ROLES = ["lead", "senior", "junior", "intern", "artist", "designer"]

    def __init__(
        self,
        name: str,
        role: str = "junior",
        user_id: Optional[str] = None,
        email: Optional[str] = None,
        created_at: Optional[str] = None,
        projects: Optional[List[str]] = None,
    ):
        """Initialize a User.

        Args:
            name: Name of the developer
            role: Developer role (default: junior)
            user_id: Unique identifier (auto-generated if None)
            email: Developer's email
            created_at: Creation timestamp (auto-generated if None)
            projects: List of project IDs (default: empty)
        """
        self.user_id = user_id or self._generate_id()
        self.name = name
        self.role = role if role in self.VALID_ROLES else "junior"
        self.email = email
        self.created_at = created_at or datetime.now().isoformat()
        self.projects = projects or []

    @staticmethod
    def _generate_id() -> str:
        """Generate a unique user ID."""
        from datetime import datetime

        return f"user_{datetime.now().timestamp()}"

    def add_project(self, project_id: str) -> None:
        """Add a project to the user's list.

        Args:
            project_id: ID of the project to add
        """
        if project_id not in self.projects:
            self.projects.append(project_id)

    def remove_project(self, project_id: str) -> bool:
        """Remove a project from the user's list.

        Args:
            project_id: ID of the project to remove

        Returns:
            True if project was removed, False if not found
        """
        if project_id in self.projects:
            self.projects.remove(project_id)
            return True
        return False

    def get_project_count(self) -> int:
        """Get the number of projects this user is involved in."""
        return len(self.projects)

    def to_dict(self) -> dict:
        """Convert user to dictionary representation."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "role": self.role,
            "email": self.email,
            "created_at": self.created_at,
            "projects": self.projects,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Create User from dictionary representation."""
        return cls(
            name=data["name"],
            role=data.get("role", "junior"),
            user_id=data.get("user_id"),
            email=data.get("email"),
            created_at=data.get("created_at"),
            projects=data.get("projects", []),
        )

    def __repr__(self) -> str:
        return f"User({self.user_id}: {self.name} - {self.role})"
