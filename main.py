"""Main entry point for Game Dev Studio CLI."""

import argparse
import sys
import os

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import StudioDataManager
from cli.commands import (
    cmd_add_user,
    cmd_list_users,
    cmd_view_user,
    cmd_add_project,
    cmd_list_projects,
    cmd_view_project,
    cmd_add_task,
    cmd_list_tasks,
    cmd_update_status,
    cmd_assign_task,
    cmd_studio_report,
)


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="🎮 Game Dev Studio CLI - Manage your game development projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  studio add-user --name "Alice" --role lead
  studio add-project --user "Alice" --title "Awesome Game"
  studio add-task --project "Awesome Game" --title "Create main menu"
  studio update-status --task "Create main menu" --status in-progress
  studio studio-report
        """,
    )

    # Add version
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    # Create subparsers for commands
    subparsers = parser.add_subparsers(title="commands", dest="command", help="Available commands")

    # ==================== USER COMMANDS ====================
    # add-user
    add_user_parser = subparsers.add_parser("add-user", help="Add a new user to the studio")
    add_user_parser.add_argument("--name", required=True, help="Name of the developer")
    add_user_parser.add_argument(
        "--role",
        choices=["lead", "senior", "junior", "intern", "artist", "designer"],
        default="junior",
        help="Developer role (default: junior)",
    )
    add_user_parser.add_argument("--email", help="Developer's email address")
    add_user_parser.set_defaults(func=cmd_add_user)

    # list-users
    list_users_parser = subparsers.add_parser("list-users", help="List all users in the studio")
    list_users_parser.set_defaults(func=cmd_list_users)

    # view-user
    view_user_parser = subparsers.add_parser("view-user", help="View details of a specific user")
    view_user_parser.add_argument("user", help="Name of the user to view")
    view_user_parser.set_defaults(func=cmd_view_user)

    # ==================== PROJECT COMMANDS ====================
    # add-project
    add_project_parser = subparsers.add_parser(
        "add-project", help="Add a new project to the studio"
    )
    add_project_parser.add_argument("--user", required=True, help="Name of the project lead")
    add_project_parser.add_argument("--title", required=True, help="Title of the game/project")
    add_project_parser.add_argument(
        "--description", default="", help="Project description"
    )
    add_project_parser.set_defaults(func=cmd_add_project)

    # list-projects
    list_projects_parser = subparsers.add_parser(
        "list-projects", help="List all projects in the studio"
    )
    list_projects_parser.add_argument(
        "--user", help="Filter projects by user name (optional)"
    )
    list_projects_parser.set_defaults(func=cmd_list_projects)

    # view-project
    view_project_parser = subparsers.add_parser(
        "view-project", help="View details of a specific project"
    )
    view_project_parser.add_argument("project", help="Title of the project to view")
    view_project_parser.set_defaults(func=cmd_view_project)

    # ==================== TASK COMMANDS ====================
    # add-task
    add_task_parser = subparsers.add_parser("add-task", help="Add a new task to a project")
    add_task_parser.add_argument("--project", required=True, help="Title of the project")
    add_task_parser.add_argument("--title", required=True, help="Title of the task/feature")
    add_task_parser.set_defaults(func=cmd_add_task)

    # list-tasks
    list_tasks_parser = subparsers.add_parser("list-tasks", help="List all tasks in the studio")
    list_tasks_parser.add_argument(
        "--project", help="Filter tasks by project title (optional)"
    )
    list_tasks_parser.set_defaults(func=cmd_list_tasks)

    # update-status
    update_status_parser = subparsers.add_parser(
        "update-status", help="Update the status of a task"
    )
    update_status_parser.add_argument("--task", required=True, help="Title of the task")
    update_status_parser.add_argument(
        "--status",
        required=True,
        choices=["backlog", "in-progress", "playtesting", "shipped"],
        help="New status for the task",
    )
    update_status_parser.set_defaults(func=cmd_update_status)

    # assign-task
    assign_task_parser = subparsers.add_parser("assign-task", help="Assign a task to a user")
    assign_task_parser.add_argument("--task", required=True, help="Title of the task")
    assign_task_parser.add_argument("--user", required=True, help="Name of the user")
    assign_task_parser.set_defaults(func=cmd_assign_task)

    # ==================== REPORT COMMANDS ====================
    # studio-report
    studio_report_parser = subparsers.add_parser(
        "studio-report", help="Generate a report of shipped games"
    )
    studio_report_parser.set_defaults(func=cmd_studio_report)

    return parser


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # If no command provided, show help
    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Initialize the data manager
    try:
        manager = StudioDataManager()
    except Exception as e:
        print(f"Failed to initialize data manager: {e}")
        sys.exit(1)

    # Execute the command
    try:
        args.func(args, manager)
    except Exception as e:
        print(f"Error executing command: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
