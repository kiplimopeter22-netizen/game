"""Tests for User model."""

import pytest
from models import User


class TestUserInitialization:
    """Test User initialization."""

    def test_user_creation_with_defaults(self):
        """Test creating a user with default values."""
        user = User(name="Alice")
        assert user.name == "Alice"
        assert user.role == "junior"
        assert user.email is None
        assert user.projects == []

    def test_user_creation_with_all_fields(self):
        """Test creating a user with all fields specified."""
        user = User(
            name="Bob",
            role="lead",
            email="bob@studio.com",
            user_id="user_123",
        )
        assert user.name == "Bob"
        assert user.role == "lead"
        assert user.email == "bob@studio.com"
        assert user.user_id == "user_123"

    def test_invalid_role_defaults_to_junior(self):
        """Test that invalid roles default to junior."""
        user = User(name="Charlie", role="invalid_role")
        assert user.role == "junior"


class TestUserMethods:
    """Test User methods."""

    def test_add_project(self):
        """Test adding a project to a user."""
        user = User(name="Dave")
        user.add_project("proj_1")
        assert "proj_1" in user.projects
        assert user.get_project_count() == 1

    def test_add_duplicate_project(self):
        """Test that duplicate projects are not added twice."""
        user = User(name="Eve")
        user.add_project("proj_1")
        user.add_project("proj_1")
        assert user.get_project_count() == 1

    def test_remove_project(self):
        """Test removing a project from a user."""
        user = User(name="Frank", projects=["proj_1", "proj_2"])
        assert user.remove_project("proj_1") is True
        assert "proj_1" not in user.projects
        assert user.get_project_count() == 1

    def test_remove_nonexistent_project(self):
        """Test removing a project that doesn't exist."""
        user = User(name="Grace")
        assert user.remove_project("proj_1") is False


class TestUserSerialization:
    """Test User serialization."""

    def test_to_dict(self):
        """Test converting user to dictionary."""
        user = User(name="Henry", role="senior", email="henry@studio.com")
        user_dict = user.to_dict()
        assert user_dict["name"] == "Henry"
        assert user_dict["role"] == "senior"
        assert user_dict["email"] == "henry@studio.com"

    def test_from_dict(self):
        """Test creating user from dictionary."""
        data = {
            "name": "Iris",
            "role": "lead",
            "email": "iris@studio.com",
            "user_id": "user_789",
            "projects": ["proj_1", "proj_2"],
        }
        user = User.from_dict(data)
        assert user.name == "Iris"
        assert user.role == "lead"
        assert user.user_id == "user_789"
        assert len(user.projects) == 2
