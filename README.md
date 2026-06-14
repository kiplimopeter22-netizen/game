# 🎮 Game Dev Studio CLI

A command-line interface tool for managing a game development studio's projects, team members, and tasks. Built with Python 3.10+ using object-oriented design patterns, argparse for CLI, JSON for persistence, and the `rich` library for beautiful terminal output.

## Features

- **User Management**: Create and manage developer roles (lead, senior, junior, intern, artist, designer)
- **Project Management**: Organize games/projects with leads and descriptions
- **Task Tracking**: Add features as tasks with status flow: `backlog → in-progress → playtesting → shipped`
- **Task Assignment**: Assign tasks to team members
- **Studio Reporting**: Generate reports on shipped games and team progress
- **Data Persistence**: All data saved to JSON for consistency across sessions
- **Rich CLI Output**: Beautiful colored tables and panels for easy visualization

## Project Structure

```
game/
├── models/                 # Core data models
│   ├── __init__.py
│   ├── user.py            # User class
│   ├── project.py         # Project class
│   └── task.py            # Task class
├── cli/                    # Command-line interface
│   ├── __init__.py
│   └── commands.py        # CLI command implementations
├── data/                   # Data storage
│   └── studio.json        # Persisted studio data
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_user.py       # User model tests
│   ├── test_project.py    # Project model tests
│   ├── test_task.py       # Task model tests
│   ├── test_persistence.py # Data manager tests
│   └── test_cli.py        # CLI command tests
├── utils.py               # Data manager and utilities
├── main.py                # CLI entry point
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd game
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the CLI

The tool is executed via the `main.py` script with subcommands for different operations.

```bash
python main.py [command] [options]
```

### Available Commands

#### User Management

**Add a new user:**
```bash
python main.py add-user --name "Alice" --role lead --email "alice@studio.com"
```

**List all users:**
```bash
python main.py list-users
```

**View user details:**
```bash
python main.py view-user "Alice"
```

#### Project Management

**Add a new project:**
```bash
python main.py add-project --user "Alice" --title "Awesome Game" --description "An epic adventure"
```

**List all projects:**
```bash
python main.py list-projects
```

**List projects by a specific user:**
```bash
python main.py list-projects --user "Alice"
```

**View project details:**
```bash
python main.py view-project "Awesome Game"
```

#### Task Management

**Add a task to a project:**
```bash
python main.py add-task --project "Awesome Game" --title "Create main menu"
```

**List all tasks:**
```bash
python main.py list-tasks
```

**List tasks in a project:**
```bash
python main.py list-tasks --project "Awesome Game"
```

**Update task status:**
```bash
python main.py update-status --task "Create main menu" --status in-progress
```

Valid statuses: `backlog`, `in-progress`, `playtesting`, `shipped`

**Assign task to a user:**
```bash
python main.py assign-task --task "Create main menu" --user "Bob"
```

#### Reports

**Generate studio report:**
```bash
python main.py studio-report
```

Shows overall studio statistics and lists all shipped games.

## Data Persistence

All data is automatically saved to `data/studio.json` in JSON format. The data structure includes:

```json
{
  "users": {
    "user_id": {
      "user_id": "...",
      "name": "...",
      "role": "...",
      "email": "...",
      "created_at": "...",
      "projects": [...]
    }
  },
  "projects": {
    "project_id": {
      "project_id": "...",
      "title": "...",
      "user_id": "...",
      "description": "...",
      "created_at": "...",
      "tasks": [...]
    }
  },
  "tasks": {
    "task_id": {
      "task_id": "...",
      "title": "...",
      "project_id": "...",
      "status": "...",
      "assigned_to": "...",
      "created_at": "..."
    }
  }
}
```

## Architecture

### Object-Oriented Design

The project uses a clean OOP architecture with three core model classes:

- **User**: Represents a developer with a role, email, and list of projects
- **Project**: Represents a game with a lead developer, description, and list of tasks
- **Task**: Represents a feature with a status, assignment, and project reference

### Data Manager

`StudioDataManager` handles all persistence operations:
- Loads data from JSON on initialization
- Saves data after any modification
- Provides methods for CRUD operations on all entities
- Maintains data relationships (users to projects, projects to tasks)

### CLI Implementation

Uses Python's `argparse` module to:
- Define subcommands for each operation
- Validate arguments
- Display helpful error messages
- Route commands to appropriate handlers

### Rich Library Integration

The `rich` library provides:
- Colored terminal output
- Formatted tables for data display
- Panels for detailed information
- Emoji icons for visual feedback

## Testing

Run the test suite with pytest:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_user.py

# Run with coverage
pytest --cov=.
```

Test files include:
- `test_user.py`: User model creation, methods, and serialization
- `test_project.py`: Project model and task management
- `test_task.py`: Task status transitions and assignments
- `test_persistence.py`: Data manager and JSON persistence
- `test_cli.py`: CLI command execution and output

## Example Workflow

Here's a typical workflow using the CLI:

```bash
# 1. Add team members
python main.py add-user --name "Alice" --role lead
python main.py add-user --name "Bob" --role senior
python main.py add-user --name "Charlie" --role junior

# 2. Create a project
python main.py add-project --user "Alice" --title "Epic Quest" --description "A fantasy RPG"

# 3. Add tasks
python main.py add-task --project "Epic Quest" --title "Design characters"
python main.py add-task --project "Epic Quest" --title "Implement battle system"
python main.py add-task --project "Epic Quest" --title "Create UI mockups"

# 4. Assign tasks
python main.py assign-task --task "Design characters" --user "Bob"
python main.py assign-task --task "Implement battle system" --user "Charlie"

# 5. Update task status
python main.py update-status --task "Design characters" --status in-progress
python main.py update-status --task "Design characters" --status playtesting
python main.py update-status --task "Design characters" --status shipped

# 6. View progress
python main.py view-project "Epic Quest"
python main.py studio-report
```

## Dependencies

- **rich** (^13.0.0): Terminal formatting and beautiful output
- **pytest** (^7.0.0): Testing framework

## Requirements Met

✅ **Object-Oriented Design** (20 pts): Classes for User, Project, Task with clear relationships
✅ **Command-Line Interface** (20 pts): Full argparse implementation with subcommands
✅ **Persistence with File I/O** (20 pts): JSON-based data persistence
✅ **Code Structure & Reusability** (15 pts): Modular design with clear separation of concerns
✅ **External Package Usage** (10 pts): Rich library for enhanced CLI output
✅ **Testing & Debugging** (10 pts): Comprehensive pytest suite with multiple test modules
✅ **Git Workflow & Management** (5 pts): Regular commits with meaningful messages

## License

MIT License - Feel free to use and modify this project.

## Author

Created as a summative lab for game development studio project management.
