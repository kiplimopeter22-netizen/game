"""CLI commands for Game Dev Studio."""

import sys
from typing import Optional

from models import User, Project, Task
from utils import StudioDataManager

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel

    HAS_RICH = True
except ImportError:
    HAS_RICH = False

console = Console() if HAS_RICH else None


def print_error(message: str) -> None:
    """Print an error message."""
    if HAS_RICH:
        console.print(f"[bold red]❌ Error:[/bold red] {message}")
    else:
        print(f"ERROR: {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    if HAS_RICH:
        console.print(f"[bold green]✓ Success:[/bold green] {message}")
    else:
        print(f"SUCCESS: {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    if HAS_RICH:
        console.print(f"[bold blue]ℹ️  Info:[/bold blue] {message}")
    else:
        print(f"INFO: {message}")


# User Commands
def cmd_add_user(args, manager: StudioDataManager) -> None:
    """Add a new user to the studio."""
    user = User(name=args.name, role=args.role, email=args.email)
    if manager.add_user(user):
        print_success(f'User "{args.name}" ({args.role}) added with ID: {user.user_id}')
    else:
        print_error(f'Failed to add user "{args.name}"')


def cmd_list_users(args, manager: StudioDataManager) -> None:
    """List all users in the studio."""
    users = manager.list_users()
    if not users:
        print_info("No users found")
        return

    if HAS_RICH:
        table = Table(title="Studio Team Members")
        table.add_column("User ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Role", style="yellow")
        table.add_column("Email", style="green")
        table.add_column("Projects", style="blue")

        for user in users:
            table.add_row(
                user.user_id,
                user.name,
                user.role,
                user.email or "N/A",
                str(user.get_project_count()),
            )
        console.print(table)
    else:
        print("Studio Team Members:")
        for user in users:
            print(
                f"  {user.user_id}: {user.name} ({user.role}) - {user.get_project_count()} projects"
            )


def cmd_view_user(args, manager: StudioDataManager) -> None:
    """View details of a specific user."""
    user = manager.get_user_by_name(args.user)
    if not user:
        print_error(f'User "{args.user}" not found')
        return

    projects = manager.list_user_projects(user.user_id)

    if HAS_RICH:
        panel_text = (
            f"[bold]ID:[/bold] {user.user_id}\n"
            f"[bold]Name:[/bold] {user.name}\n"
            f"[bold]Role:[/bold] {user.role}\n"
            f"[bold]Email:[/bold] {user.email or 'N/A'}\n"
            f"[bold]Projects:[/bold] {len(projects)}"
        )
        console.print(Panel(panel_text, title=user.name, expand=False))

        if projects:
            table = Table(title="Assigned Projects")
            table.add_column("Project ID", style="cyan")
            table.add_column("Title", style="magenta")
            table.add_column("Tasks", style="blue")
            for project in projects:
                table.add_row(
                    project.project_id, project.title, str(len(project.tasks))
                )
            console.print(table)
    else:
        print(f"\nUser: {user.name}")
        print(f"  ID: {user.user_id}")
        print(f"  Role: {user.role}")
        print(f"  Email: {user.email or 'N/A'}")
        print(f"  Projects: {len(projects)}")
        if projects:
            print("  Projects:")
            for p in projects:
                print(f"    - {p.title} ({len(p.tasks)} tasks)")


# Project Commands
def cmd_add_project(args, manager: StudioDataManager) -> None:
    """Add a new project to the studio."""
    user = manager.get_user_by_name(args.user)
    if not user:
        print_error(f'User "{args.user}" not found')
        return

    project = Project(
        title=args.title, user_id=user.user_id, description=args.description
    )
    if manager.add_project(project):
        print_success(
            f'Project "{args.title}" added by {user.name} with ID: {project.project_id}'
        )
    else:
        print_error(f'Failed to add project "{args.title}"')


def cmd_list_projects(args, manager: StudioDataManager) -> None:
    """List all projects or projects by a user."""
    if args.user:
        user = manager.get_user_by_name(args.user)
        if not user:
            print_error(f'User "{args.user}" not found')
            return
        projects = manager.list_user_projects(user.user_id)
        title = f'Projects by {user.name}'
    else:
        projects = manager.list_projects()
        title = "All Studio Projects"

    if not projects:
        print_info("No projects found")
        return

    if HAS_RICH:
        table = Table(title=title)
        table.add_column("Project ID", style="cyan")
        table.add_column("Title", style="magenta")
        table.add_column("Lead", style="green")
        table.add_column("Description", style="yellow")
        table.add_column("Tasks", style="blue")

        for project in projects:
            lead = manager.get_user(project.user_id)
            table.add_row(
                project.project_id,
                project.title,
                lead.name if lead else "Unknown",
                project.description[:30] + "..."
                if len(project.description) > 30
                else project.description,
                str(len(project.tasks)),
            )
        console.print(table)
    else:
        print(f"\n{title}:")
        for project in projects:
            lead = manager.get_user(project.user_id)
            print(
                f"  {project.project_id}: {project.title} (Lead: {lead.name if lead else 'Unknown'})"
            )
            print(f"    Description: {project.description}")
            print(f"    Tasks: {len(project.tasks)}")


def cmd_view_project(args, manager: StudioDataManager) -> None:
    """View details of a specific project."""
    project = manager.get_project_by_title(args.project)
    if not project:
        print_error(f'Project "{args.project}" not found')
        return

    lead = manager.get_user(project.user_id)
    tasks = manager.list_project_tasks(project.project_id)

    if HAS_RICH:
        panel_text = (
            f"[bold]ID:[/bold] {project.project_id}\n"
            f"[bold]Title:[/bold] {project.title}\n"
            f"[bold]Lead:[/bold] {lead.name if lead else 'Unknown'}\n"
            f"[bold]Description:[/bold] {project.description or 'N/A'}\n"
            f"[bold]Tasks:[/bold] {len(tasks)}"
        )
        console.print(Panel(panel_text, title=project.title, expand=False))

        if tasks:
            table = Table(title="Project Tasks")
            table.add_column("Task ID", style="cyan")
            table.add_column("Title", style="magenta")
            table.add_column("Status", style="yellow")
            table.add_column("Assigned To", style="green")
            for task in tasks:
                assigned = manager.get_user(task.assigned_to) if task.assigned_to else None
                table.add_row(
                    task.task_id,
                    task.title,
                    task.status,
                    assigned.name if assigned else "Unassigned",
                )
            console.print(table)
    else:
        print(f"\nProject: {project.title}")
        print(f"  ID: {project.project_id}")
        print(f"  Lead: {lead.name if lead else 'Unknown'}")
        print(f"  Description: {project.description or 'N/A'}")
        print(f"  Tasks: {len(tasks)}")


# Task Commands
def cmd_add_task(args, manager: StudioDataManager) -> None:
    """Add a new task to a project."""
    project = manager.get_project_by_title(args.project)
    if not project:
        print_error(f'Project "{args.project}" not found')
        return

    task = Task(title=args.title, project_id=project.project_id)
    if manager.add_task(task):
        print_success(
            f'Task "{args.title}" added to {project.title} with ID: {task.task_id}'
        )
    else:
        print_error(f'Failed to add task "{args.title}"')


def cmd_list_tasks(args, manager: StudioDataManager) -> None:
    """List all tasks or tasks in a project."""
    if args.project:
        project = manager.get_project_by_title(args.project)
        if not project:
            print_error(f'Project "{args.project}" not found')
            return
        tasks = manager.list_project_tasks(project.project_id)
        title = f'Tasks in "{project.title}"'
    else:
        tasks = manager.list_tasks()
        title = "All Studio Tasks"

    if not tasks:
        print_info("No tasks found")
        return

    if HAS_RICH:
        table = Table(title=title)
        table.add_column("Task ID", style="cyan")
        table.add_column("Title", style="magenta")
        table.add_column("Project", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Assigned To", style="blue")

        for task in tasks:
            project = manager.get_project(task.project_id)
            assigned = manager.get_user(task.assigned_to) if task.assigned_to else None
            table.add_row(
                task.task_id,
                task.title,
                project.title if project else "Unknown",
                task.status,
                assigned.name if assigned else "Unassigned",
            )
        console.print(table)
    else:
        print(f"\n{title}:")
        for task in tasks:
            project = manager.get_project(task.project_id)
            assigned = manager.get_user(task.assigned_to) if task.assigned_to else None
            print(f"  {task.task_id}: {task.title}")
            print(f"    Project: {project.title if project else 'Unknown'}")
            print(f"    Status: {task.status}")
            print(f"    Assigned: {assigned.name if assigned else 'Unassigned'}")


def cmd_update_status(args, manager: StudioDataManager) -> None:
    """Update the status of a task."""
    # Find task by title
    task = None
    for t in manager.list_tasks():
        if t.title.lower() == args.task.lower():
            task = t
            break

    if not task:
        print_error(f'Task "{args.task}" not found')
        return

    if manager.update_task(task.task_id, status=args.status):
        print_success(
            f'Task "{args.task}" status updated to "{args.status}"'
        )
    else:
        print_error(f'Invalid status "{args.status}"')


def cmd_assign_task(args, manager: StudioDataManager) -> None:
    """Assign a task to a user."""
    # Find task by title
    task = None
    for t in manager.list_tasks():
        if t.title.lower() == args.task.lower():
            task = t
            break

    if not task:
        print_error(f'Task "{args.task}" not found')
        return

    user = manager.get_user_by_name(args.user)
    if not user:
        print_error(f'User "{args.user}" not found')
        return

    if manager.update_task(task.task_id, assigned_to=user.user_id):
        print_success(f'Task "{args.task}" assigned to {user.name}')
    else:
        print_error(f'Failed to assign task')


# Report Commands
def cmd_studio_report(args, manager: StudioDataManager) -> None:
    """Generate a studio report with shipped games."""
    all_projects = manager.list_projects()
    shipped_projects = []

    for project in all_projects:
        tasks = manager.list_project_tasks(project.project_id)
        if tasks:
            all_shipped = all(task.status == "shipped" for task in tasks)
            if all_shipped:
                shipped_projects.append(project)

    if HAS_RICH:
        console.print("[bold cyan]" + "=" * 50 + "[/bold cyan]")
        console.print("[bold green]🎮 STUDIO REPORT 🎮[/bold green]")
        console.print("[bold cyan]" + "=" * 50 + "[/bold cyan]")

        # Studio stats
        total_users = len(manager.list_users())
        total_projects = len(all_projects)
        total_tasks = len(manager.list_tasks())
        total_shipped = len(shipped_projects)

        stats_text = (
            f"[bold]Total Team Members:[/bold] {total_users}\n"
            f"[bold]Total Projects:[/bold] {total_projects}\n"
            f"[bold]Total Features:[/bold] {total_tasks}\n"
            f"[bold]Games Shipped:[/bold] {total_shipped}"
        )
        console.print(Panel(stats_text, title="Studio Stats"))

        if shipped_projects:
            table = Table(title="Shipped Games 🚀")
            table.add_column("Game Title", style="magenta")
            table.add_column("Lead Developer", style="cyan")
            table.add_column("Features", style="green")

            for project in shipped_projects:
                lead = manager.get_user(project.user_id)
                table.add_row(
                    project.title, lead.name if lead else "Unknown", str(len(project.tasks))
                )
            console.print(table)
        else:
            console.print("[yellow]No shipped games yet![/yellow]")

        console.print("[bold cyan]" + "=" * 50 + "[/bold cyan]")
    else:
        print("=" * 50)
        print("STUDIO REPORT")
        print("=" * 50)
        print(f"Total Team Members: {total_users}")
        print(f"Total Projects: {total_projects}")
        print(f"Total Features: {total_tasks}")
        print(f"Games Shipped: {total_shipped}")

        if shipped_projects:
            print("\nShipped Games:")
            for project in shipped_projects:
                lead = manager.get_user(project.user_id)
                print(f"  - {project.title} (Lead: {lead.name if lead else 'Unknown'})")
        else:
            print("\nNo shipped games yet!")

        print("=" * 50)
