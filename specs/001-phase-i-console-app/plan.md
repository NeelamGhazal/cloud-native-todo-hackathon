# Implementation Plan: Phase I - Todo In-Memory Python Console App

**Branch**: `001-phase-i-console-app` | **Date**: 2025-12-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase-i-console-app/spec.md`

## Summary

Build a command-line todo application using Python 3.13+ with in-memory task storage, demonstrating spec-driven development workflow. The application provides 5 core features (add, view, update, delete, toggle completion) through a command-based CLI interface with slash prefix commands (/add, /list, etc.). Tasks are stored as dataclass instances in a list, with interactive prompts for user input and automatic whitespace trimming/validation.

**Technical Approach**: Modular architecture with separation of concerns (models.py, cli.py, main.py), dataclass-based Task model, manual command parsing, simple linear list storage, and validation-first error handling.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (dataclasses, typing)
**Storage**: In-memory Python list (no persistence, data lost on exit)
**Testing**: Manual CLI testing (no automated test framework in Phase I)
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows via WSL 2)
**Project Type**: Single project (console application)
**Performance Goals**: Instant response for all operations (in-memory, no I/O)
**Constraints**:
  - No external dependencies (standard library only)
  - No file/database persistence
  - Maximum title: 200 characters
  - Maximum description: 1000 characters
  - In-memory only (stateless across runs)
**Scale/Scope**:
  - Single user per session
  - Designed for 1-100 tasks (linear search acceptable)
  - 5 core commands + help/exit
  - ~300-500 lines of code total

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **Spec-Driven Development**: All code generated from specifications (zero manual coding)
✅ **Progressive Complexity**: Phase I foundation for Phase II web app
✅ **Technology Stack**: Python 3.13+, UV package manager (as mandated)
✅ **No Manual Coding**: Implementation via Claude Code from tasks
✅ **Deliverables**: src/, specs/, CLAUDE.md, README.md present
✅ **Phase I Requirements**: All 5 Basic Level features covered (Add, View, Update, Delete, Mark Complete)

**Gate Status**: ✅ PASS - No violations

## Project Structure

### Documentation (this feature)

```text
specs/001-phase-i-console-app/
├── spec.md              # Feature specification (✅ complete)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technical decisions)
├── data-model.md        # Phase 1 output (Task dataclass spec)
├── quickstart.md        # Phase 1 output (setup & usage guide)
├── contracts/           # Phase 1 output (CLI command specs)
│   ├── add-command.md
│   ├── list-command.md
│   ├── update-command.md
│   ├── delete-command.md
│   ├── complete-command.md
│   └── help-exit-commands.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── __init__.py          # Package marker
├── models.py            # Task dataclass definition
├── operations.py        # CRUD operations (TaskManager class)
├── validators.py        # Input validation and sanitization
└── main.py              # CLI entry point, command loop

pyproject.toml           # UV project configuration
README.md                # Setup and usage instructions
CLAUDE.md                # Claude Code agent instructions
```

**Structure Decision**: Single project structure chosen (Option 1) as this is a console application with no web/mobile components. The modular file organization (models, operations, validators, main) provides clear separation of concerns while maintaining simplicity for a CLI tool. This structure prepares for Phase II evolution where models.py can become SQLModel and operations.py can become FastAPI routes.

## Complexity Tracking

> **No violations - this section intentionally left empty per Constitution Check pass.**

---

## Phase 0: Research & Technical Decisions

### Research Tasks

1. **Python 3.13 Type Hints Best Practices**
   - Decision: Use Python 3.13 type parameter syntax where beneficial, fall back to `typing` module for complex types
   - Rationale: Python 3.13 provides cleaner syntax for generics (`list[Task]` vs `List[Task]`), but `typing` module needed for `Optional`, `Callable`, etc.
   - Alternatives considered: Stick to `typing` module entirely (rejected: verbose), use no type hints (rejected: violates code quality standards)

2. **Command Parsing Approach**
   - Decision: Manual string parsing with simple `split()` and pattern matching
   - Rationale: Only 6 commands (/add, /list, /update, /delete, /complete, /exit); argparse is overkill and adds complexity
   - Alternatives considered: argparse library (rejected: too heavy), cmd module (rejected: interactive menu pattern)
   - Implementation: `command = input().strip().lower().split()[0]` → match/case statement

3. **Task Storage: List vs Dict**
   - Decision: `tasks: list[Task]` with linear search by ID
   - Rationale: Simple, maintains insertion order, O(n) lookup acceptable for <100 tasks, clean iteration for /list command
   - Alternatives considered: `dict[int, Task]` with O(1) lookup (rejected: ordering complexity, premature optimization)

4. **Error Handling Pattern**
   - Decision: Return `None` on errors, validate at CLI layer before calling operations
   - Rationale: Simpler control flow, no exception hierarchy needed, explicit error checking promotes clarity
   - Alternatives considered: Custom exceptions (rejected: overhead for 5 commands), silent failures (rejected: poor UX)
   - Pattern: `task = manager.get_by_id(task_id); if task is None: print("Task #X not found")`

5. **CLI Output Formatting**
   - Decision: Simple `print()` statements with manual formatting
   - Rationale: No external dependencies (rich/tabulate), focus on logic over presentation, sufficient for Phase I
   - Alternatives considered: Rich library tables (rejected: external dep), ASCII art (rejected: complexity)
   - Format: `{id} | {status} | {title[:50]} | {description[:50]}`

6. **Input Validation Strategy**
   - Decision: Validators module with pure functions (`validate_title(s: str) -> tuple[bool, str]`)
   - Rationale: Reusable across commands, testable in isolation, clear separation from business logic
   - Pattern: All validators return `(is_valid: bool, message: str)` tuple

7. **ID Generation**
   - Decision: Auto-increment counter in TaskManager, starting from 1, reset each run
   - Rationale: Simple, predictable, no UUID overhead, acceptable for in-memory Phase I
   - Implementation: `self.next_id += 1` after each add

8. **Empty Description Handling**
   - Decision: Allow empty string `""` as default, optional field
   - Rationale: Description is optional per spec, empty string simpler than `None`
   - Validation: No minimum length check for description (only maximum 1000 chars)

### Research Output

See `research.md` for full decision rationale and alternatives analysis.

---

## Phase 1: Design & Contracts

### Data Model

See `data-model.md` for complete specification. Summary:

**Task Entity** (`@dataclass`):
```python
@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
```

**Validation Rules**:
- `title`: 1-200 characters (after trim), required, non-whitespace-only
- `description`: 0-1000 characters (after trim), optional
- `completed`: boolean, defaults to `False`
- `id`: positive integer, auto-generated, unique within session

**State Transitions**:
- `completed`: `False` ↔ `True` (toggle via /complete command)

### API Contracts

See `contracts/` directory for detailed command specifications. Summary:

| Command | Args | Prompts | Success Output | Error Conditions |
|---------|------|---------|----------------|------------------|
| `/add` | None | Title, Description | `Task #X added: {title}` | Empty title, >200 chars, >1000 desc |
| `/list` | None | None | Table of tasks or "No tasks yet. Add one with /add" | None |
| `/update` | ID | New title (y/n), New desc (y/n) | `Task #X updated` | Task not found, no fields selected, validation failures |
| `/delete` | ID | Confirm (y/n) | `Task #X deleted` | Task not found, declined confirmation |
| `/complete` | ID | None | `Task #X marked complete/incomplete` | Task not found |
| `/help` | None | None | List of commands | None |
| `/exit` | None | None | Program terminates | None |

### Component Design

**1. TaskManager Class** (`operations.py`):
```python
class TaskManager:
    def __init__(self):
        self.tasks: list[Task] = []
        self.next_id: int = 1

    def add(self, title: str, description: str = "") -> Task
    def get_all(self) -> list[Task]
    def get_by_id(self, task_id: int) -> Task | None
    def update(self, task_id: int, title: str | None, description: str | None) -> Task | None
    def delete(self, task_id: int) -> bool
    def toggle_complete(self, task_id: int) -> Task | None
```

**2. Validators** (`validators.py`):
```python
def sanitize_input(text: str) -> str
    """Trim leading/trailing whitespace."""

def validate_title(title: str) -> tuple[bool, str]
    """Check 1-200 chars, non-empty after trim."""

def validate_description(desc: str) -> tuple[bool, str]
    """Check 0-1000 chars."""

def validate_task_id(id_str: str) -> tuple[bool, int | None, str]
    """Parse and validate integer > 0."""
```

**3. CLI Interface** (`main.py`):
```python
def main_loop(manager: TaskManager) -> None
    """Command loop until /exit."""

def handle_add(manager: TaskManager) -> None
def handle_list(manager: TaskManager) -> None
def handle_update(manager: TaskManager) -> None
def handle_delete(manager: TaskManager) -> None
def handle_complete(manager: TaskManager) -> None
def handle_help() -> None
```

### Command Flow Diagrams

**Add Command**:
```
User: /add
  → main_loop: parse command
  → handle_add()
    → prompt: "Title: "
    → input: user enters title
    → validators.sanitize_input(title)
    → validators.validate_title(title)
    → if invalid: print error, retry
    → prompt: "Description (optional): "
    → input: user enters description
    → validators.sanitize_input(description)
    → validators.validate_description(description)
    → if invalid: print error, retry
    → manager.add(title, description)
    → print: "Task #{id} added: {title}"
```

**List Command**:
```
User: /list
  → main_loop: parse command
  → handle_list()
    → tasks = manager.get_all()
    → if len(tasks) == 0:
      → print: "No tasks yet. Add one with /add"
    → else:
      → print header: "ID | Status | Title | Description"
      → for task in tasks:
        → status = "✓ Complete" if task.completed else "✗ Incomplete"
        → print: f"{task.id} | {status} | {task.title[:50]} | {task.description[:50]}"
```

**Update Command**:
```
User: /update
  → main_loop: parse command
  → handle_update()
    → prompt: "Task ID: "
    → input: user enters ID
    → validators.validate_task_id(id_str)
    → if invalid: print error, return
    → task = manager.get_by_id(task_id)
    → if task is None: print "Task #{id} not found", return
    → prompt: "Update title? (y/n): "
    → if yes:
      → prompt: "New title: "
      → validate and sanitize
      → new_title = sanitized input
    → else: new_title = None
    → prompt: "Update description? (y/n): "
    → if yes:
      → prompt: "New description: "
      → validate and sanitize
      → new_description = sanitized input
    → else: new_description = None
    → if new_title is None and new_description is None:
      → print: "No fields selected for update"
      → return
    → manager.update(task_id, new_title, new_description)
    → print: "Task #{id} updated"
```

**Delete Command**:
```
User: /delete
  → main_loop: parse command
  → handle_delete()
    → prompt: "Task ID: "
    → validate_task_id()
    → task = manager.get_by_id(task_id)
    → if task is None: print error, return
    → print: f"Delete task #{task.id}: {task.title}?"
    → prompt: "Confirm (y/n): "
    → if not confirmed: print "Cancelled", return
    → manager.delete(task_id)
    → print: "Task #{id} deleted"
```

**Complete Command**:
```
User: /complete
  → main_loop: parse command
  → handle_complete()
    → prompt: "Task ID: "
    → validate_task_id()
    → task = manager.toggle_complete(task_id)
    → if task is None: print "Task #{id} not found", return
    → status = "complete" if task.completed else "incomplete"
    → print: f"Task #{task.id} marked {status}"
```

### Quickstart Guide

See `quickstart.md` for complete setup instructions. Summary:

**Prerequisites**:
- Python 3.13+
- UV package manager

**Setup**:
```bash
# Clone repository
git clone <repo-url>
cd hackathon-todo

# Ensure on correct branch
git checkout 001-phase-i-console-app

# Install dependencies (none for Phase I, but sets up UV environment)
uv sync

# Run application
uv run python src/main.py
```

**Usage**:
```
Available commands:
  /add       - Add a new task
  /list      - View all tasks
  /update    - Update a task
  /delete    - Delete a task
  /complete  - Toggle task completion status
  /help      - Show this help message
  /exit      - Exit the application

Example session:
> /add
Title: Fix login bug
Description (optional): Update JWT validation logic

Task #1 added: Fix login bug

> /list
ID | Status | Title | Description
1 | ✗ Incomplete | Fix login bug | Update JWT validation logic

> /complete
Task ID: 1

Task #1 marked complete

> /exit
Goodbye!
```

---

## Code Quality Standards

**Type Hints**:
```python
# Use Python 3.13 syntax for built-in generics
def get_all(self) -> list[Task]:
    return self.tasks

# Use typing module for complex types
from typing import Optional
def get_by_id(self, task_id: int) -> Task | None:
    ...
```

**Docstrings** (Google style):
```python
def add(self, title: str, description: str = "") -> Task:
    """Add a new task to the task list.

    Args:
        title: Task title (1-200 characters, required)
        description: Task description (0-1000 characters, optional)

    Returns:
        The newly created Task instance with auto-generated ID
    """
```

**Constants**:
```python
# validators.py
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000
MIN_TITLE_LENGTH = 1
```

**Naming Conventions**:
- Functions: `snake_case` (e.g., `get_by_id`, `handle_add`)
- Variables: `snake_case` (e.g., `task_id`, `new_title`)
- Classes: `PascalCase` (e.g., `Task`, `TaskManager`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_TITLE_LENGTH`)

**Function Length**:
- Maximum 20 lines per function (except `main_loop` which orchestrates)
- Extract complex logic into helpers

**Error Messages**:
```python
# Consistent format
"Task #X not found"
"Title cannot be empty"
"Title must be 1-200 characters"
"Description must be 0-1000 characters"
"Invalid task ID"
```

---

## Development Phases

### Phase 0: Setup & Models (Priority: P1)
1. Initialize UV project with pyproject.toml
2. Create src/ directory structure
3. Implement `models.py`:
   - Task dataclass with proper type hints
   - __post_init__ validation if needed
4. Implement `validators.py`:
   - sanitize_input()
   - validate_title()
   - validate_description()
   - validate_task_id()

### Phase 1: TaskManager (Priority: P1)
1. Implement `operations.py`:
   - TaskManager class initialization
   - add() method with ID generation
   - get_all() method
   - get_by_id() method with linear search
2. Manual testing of core CRUD operations

### Phase 2: CLI Skeleton (Priority: P1)
1. Implement `main.py`:
   - main_loop() with command parsing
   - handle_help() with command list
   - handle_exit() for clean termination
2. Basic command routing (match/case or if/elif)

### Phase 3: Add & List Commands (Priority: P1)
1. Implement handle_add():
   - Interactive prompts for title/description
   - Input validation and error handling
   - Success confirmation
2. Implement handle_list():
   - Empty list message
   - Formatted table output
   - Status indicator (✓/✗)

### Phase 4: Update, Delete, Complete Commands (Priority: P2)
1. Implement handle_update():
   - ID prompt and validation
   - Selective field updates (title/description/both)
   - Error handling
2. Implement handle_delete():
   - ID prompt and validation
   - Confirmation prompt
   - Success/cancellation messages
3. Implement handle_complete():
   - ID prompt and validation
   - Toggle logic
   - Status confirmation

### Phase 5: Polish & Edge Cases (Priority: P3)
1. Refine error messages
2. Handle edge cases:
   - Very long titles/descriptions (truncation in display)
   - Whitespace-only inputs
   - Invalid command inputs
3. Add input retry loops for validation failures
4. Test full user journeys

---

## Testing Strategy

**Manual Validation Checklist**:

✓ **Feature Completeness**:
- [ ] Can add task with title only
- [ ] Can add task with title + description
- [ ] Rejects empty title (after trim)
- [ ] Rejects title >200 characters
- [ ] Rejects description >1000 characters
- [ ] Can view empty task list (shows friendly message)
- [ ] Can view task list with multiple tasks
- [ ] Can update title only
- [ ] Can update description only
- [ ] Can update both title and description
- [ ] Rejects update for non-existent ID
- [ ] Can delete existing task
- [ ] Rejects delete for non-existent ID
- [ ] Can toggle task to complete
- [ ] Can toggle task to incomplete
- [ ] Task IDs auto-increment correctly
- [ ] /help shows all commands
- [ ] /exit terminates cleanly

✓ **Edge Cases**:
- [ ] Title with exactly 200 characters (boundary - should accept)
- [ ] Title with 201 characters (should reject)
- [ ] Description with exactly 1000 characters (boundary - should accept)
- [ ] Description with 1001 characters (should reject)
- [ ] Title with only whitespace (should reject after trim)
- [ ] Title with leading/trailing spaces (should trim and accept if valid)
- [ ] Invalid command (should show error + help)
- [ ] Non-integer task ID (should show error)
- [ ] Task ID = 0 (should reject)
- [ ] Negative task ID (should reject)

✓ **User Experience**:
- [ ] Error messages are clear and actionable
- [ ] Success messages confirm action taken
- [ ] /list formatting is readable
- [ ] Description preview truncates at 50 characters
- [ ] Title preview truncates at 50 characters (if needed)

---

## Risk Assessment

**Low Overall Risk**:
- Clear specification with resolved ambiguities
- Small scope (5 commands, ~300-500 LOC)
- No external dependencies
- No I/O beyond console (no network, file, DB complexity)

**Potential Issues**:
1. **Unicode/Emoji in titles**: Python 3.13 handles UTF-8 well, but character counting may differ from display width
   - Mitigation: Use `len(title)` for character count (not display width)
2. **Newlines in input**: User might paste multiline text
   - Mitigation: `sanitize_input()` can replace `\n` with space or reject
3. **Very long task lists**: Linear search degrades beyond ~1000 tasks
   - Mitigation: Acceptable for Phase I scope (designed for <100 tasks)
4. **Ctrl+C handling**: Abrupt exit might leave terminal in bad state
   - Mitigation: Not critical for Phase I, can add signal handlers later

**Mitigation Summary**:
- Input validators handle edge cases
- Clear error messages guide users
- Simplicity reduces bug surface area

---

## Success Criteria

✅ **All 5 core features functional** via CLI (/add, /list, /update, /delete, /complete)
✅ **Spec-driven development** demonstrated (100% code generated by Claude Code)
✅ **User can complete full task lifecycle** (create → view → update → mark complete → delete) in <60 seconds
✅ **Invalid inputs handled gracefully** with clear error messages (no crashes, no stack traces shown)
✅ **Data persists during runtime** (not lost between commands)
✅ **Modular code structure** (models.py, operations.py, validators.py, main.py) with clear separation of concerns
✅ **Type hints on all functions** (Python 3.13 syntax where applicable)
✅ **Deliverables complete**: src/, specs/, CLAUDE.md, README.md

---

## Next Steps

1. ✅ Specification complete (`spec.md`)
2. ✅ Clarifications resolved (5/5 questions answered)
3. ✅ Implementation plan complete (`plan.md` - this file)
4. ⏭️ Generate research.md (Phase 0 output)
5. ⏭️ Generate data-model.md (Phase 1 output)
6. ⏭️ Generate quickstart.md (Phase 1 output)
7. ⏭️ Generate contracts/ (Phase 1 output)
8. ⏭️ Run `/sp.tasks` to generate task breakdown
9. ⏭️ Run `/sp.implement` for Claude Code generation

**Recommended next command**: Continue with Phase 0 research output generation, or proceed directly to `/sp.tasks` if planning is complete.

---

**Plan Status**: ✅ Complete - Ready for task decomposition
**Branch**: `001-phase-i-console-app`
**Generated**: 2025-12-31
