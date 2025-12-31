# Cloud-Native Todo - Evolution of Todo Hackathon

Phase I: In-Memory Python Console App

A command-line todo application built using spec-driven development with Claude Code and Spec-Kit Plus.

## About

This is Phase I of the "Evolution of Todo" hackathon project, demonstrating:
- **Spec-Driven Development (SDD)**: All code generated from specifications
- **Clean Architecture**: Modular design with separation of concerns
- **Type Safety**: Python 3.13+ with comprehensive type hints
- **Progressive Evolution**: Foundation for future web, chatbot, and cloud-native phases

## Features

- ✅ **Add Tasks**: Create tasks with title and optional description
- ✅ **View Tasks**: Display all tasks with status and details
- ✅ **Update Tasks**: Modify task title and/or description
- ✅ **Delete Tasks**: Remove tasks with confirmation
- ✅ **Mark Complete**: Toggle task completion status

## Requirements

- **Python**: 3.13 or higher
- **Package Manager**: UV (recommended) or pip

## Installation

### Using UV (Recommended)

```bash
# Install UV if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone <repository-url>
cd cloud-native-todo-hackathon

# Install dependencies (currently none - standard library only)
uv sync
```

### Using pip

```bash
# Clone the repository
git clone <repository-url>
cd cloud-native-todo-hackathon

# Create virtual environment
python3.13 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Usage

### Run the Application

```bash
# Using UV
uv run todo

# Or using Python directly
python -m src.main
```

### Available Commands

Once the application is running, use these commands:

- `/add` - Add a new task (prompts for title and description)
- `/list` - View all tasks
- `/update` - Update a task by ID
- `/complete` - Toggle task completion status by ID
- `/delete` - Delete a task by ID (with confirmation)
- `/help` - Show available commands
- `/exit` - Exit the application

### Example Session

```
Welcome to Todo App! Type /help for available commands.

> /add
Enter task title: Fix authentication bug
Enter description (optional): Update JWT validation in login endpoint
✓ Task #1 added successfully

> /add
Enter task title: Write documentation
Enter description (optional):
✓ Task #2 added successfully

> /list
ID | Status | Title                    | Description
---+--------+-------------------------+----------------------------------
1  | ✗      | Fix authentication bug   | Update JWT validation in login...
2  | ✗      | Write documentation      |

> /complete
Enter task ID: 1
✓ Task #1 marked as complete

> /list
ID | Status | Title                    | Description
---+--------+-------------------------+----------------------------------
1  | ✓      | Fix authentication bug   | Update JWT validation in login...
2  | ✗      | Write documentation      |

> /exit
Goodbye!
```

## Project Structure

```
cloud-native-todo-hackathon/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── models.py            # Task dataclass definition
│   ├── operations.py        # TaskManager (CRUD operations)
│   ├── validators.py        # Input validation functions
│   └── main.py              # CLI interface and entry point
├── specs/
│   └── 001-phase-i-console-app/
│       ├── spec.md          # Feature specification
│       ├── plan.md          # Technical implementation plan
│       └── tasks.md         # Task breakdown
├── .specify/
│   └── memory/
│       └── constitution.md  # Project governance
├── pyproject.toml           # Project configuration
├── CLAUDE.md                # Agent instructions
└── README.md                # This file
```

## Design Principles

- **In-Memory Storage**: Tasks stored in Python list (no database in Phase I)
- **Command-Based CLI**: Slash-prefix commands with interactive prompts
- **Dataclass Models**: Type-safe Task representation using @dataclass
- **Validation-First**: Input sanitization and validation before operations
- **Modular Architecture**: Clear separation of models, operations, validation, and UI

## Validation Rules

- **Title**: 1-200 characters, required, whitespace-only rejected
- **Description**: 0-1000 characters, optional, defaults to empty string
- **Task ID**: Auto-incremented, starts from 1, unique within session
- **Whitespace**: Leading/trailing whitespace automatically trimmed

## Development

This project follows spec-driven development:

1. **Specification** (`/sp.specify`): Define requirements and user stories
2. **Clarification** (`/sp.clarify`): Resolve ambiguities
3. **Planning** (`/sp.plan`): Design architecture and components
4. **Tasks** (`/sp.tasks`): Break down into atomic work units
5. **Implementation** (`/sp.implement`): Generate code from tasks

All code is generated by Claude Code from specifications - zero manual coding.

## Roadmap

- **Phase I** (Current): In-memory console app ✓
- **Phase II**: Web UI with database persistence
- **Phase III**: AI chatbot integration
- **Phase IV**: Local Kubernetes deployment
- **Phase V**: Cloud-native with managed services

## Contributing

This is a hackathon project demonstrating spec-driven development. See `CLAUDE.md` for agent instructions and `.specify/memory/constitution.md` for project governance.

## License

Hackathon project - see repository for details.

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
