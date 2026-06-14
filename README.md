# Game Dev Studio CLI
Game Dev Studio CLI is a small Python command-line app for keeping track of a game studio's team, projects, and tasks.

It lets you add team members, create projects, assign work, update task statuses, and print a simple studio report. Data is saved locally in `data/studio.json`.
## Requirements
- Python 3.10 or newer
- pip
## Setup

Clone the project, move into the folder, and install the dependencies:

```bash
git clone <your-repo-url>
cd game
pip install -r requirements.txt
```

## How to use it

Run commands through `main.py`:

```bash
python main.py [command] [options]
```

Add a user:

```bash
python main.py add-user --name "Alice" --role lead --email "alice@studio.com"
```

Create a project:

```bash
python main.py add-project --user "Alice" --title "Awesome Game" --description "An epic adventure"
```

Add a task:

```bash
python main.py add-task --project "Awesome Game" --title "Create main menu"
```

Assign the task to someone:

```bash
python main.py assign-task --task "Create main menu" --user "Alice"
```

Update the task status:

```bash
python main.py update-status --task "Create main menu" --status in-progress
```

Valid statuses are `backlog`, `in-progress`, `playtesting`, and `shipped`.

## Useful commands

```bash
python main.py list-users
python main.py view-user "Alice"
python main.py list-projects
python main.py list-projects --user "Alice"
python main.py view-project "Awesome Game"
python main.py list-tasks
python main.py list-tasks --project "Awesome Game"
python main.py studio-report
```

## Project layout

```text
game/
- cli/              # Command handlers
- data/             # Local JSON data
- models/           # User, project, and task models
- tests/            # Test files
- main.py           # CLI entry point
- utils.py          # Data manager
- requirements.txt  # Dependencies
```

## Tests

Run the tests with:

```bash
pytest
```

For more detail:

```bash
pytest -v
```
