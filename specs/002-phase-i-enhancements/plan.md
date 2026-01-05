# Phase I Enhancements - Implementation Plan

**Feature:** 002-phase-i-enhancements
**Status:** Planning
**Created:** 2026-01-05
**Estimated Effort:** 12-15 hours

---

## Table of Contents
1. [Technical Context](#technical-context)
2. [Architecture Overview](#architecture-overview)
3. [Component Design](#component-design)
4. [Data Model Changes](#data-model-changes)
5. [Implementation Phases](#implementation-phases)
6. [Risk Analysis](#risk-analysis)
7. [Testing Strategy](#testing-strategy)

---

## Technical Context

### **Current Architecture**
```
src/
├── models.py          # Task dataclass
├── validators.py      # Input validation
├── operations.py      # TaskManager (CRUD)
└── main.py            # CLI interface with Rich
```

### **Technology Stack**
- **Language:** Python 3.13+
- **UI Library:** Rich (console formatting)
- **Persistence:** JSON file I/O
- **Date Parsing:** Custom implementation
- **Testing:** Manual (upgrade to pytest recommended)

### **Existing Features**
- ✅ Basic CRUD operations
- ✅ Interactive prompts
- ✅ Rich console UI
- ✅ Input validation
- ✅ In-memory task storage

---

## Architecture Overview

### **New Architecture**

```
src/
├── models.py          # Enhanced Task + Config dataclasses
├── validators.py      # Extended validation (priority, tags, dates)
├── operations.py      # TaskManager with advanced operations
├── persistence.py     # NEW: JSON save/load logic
├── parsers.py         # NEW: Command-line argument parsing
├── formatters.py      # NEW: Rich output formatting utilities
├── filters.py         # NEW: Filter and sort logic
└── main.py            # CLI with enhanced commands

.todo-data.json        # Auto-saved task data
.todo-config.json      # User configuration
```

### **Key Architectural Changes**

1. **Separation of Concerns**
   - Extract persistence logic from operations
   - Separate command parsing from main loop
   - Isolate Rich formatting into utilities

2. **Data Layer**
   - Introduce `persistence.py` for JSON I/O
   - Implement auto-save after every mutation
   - Handle file corruption gracefully

3. **Parser Layer**
   - Use `argparse` for flag-based commands
   - Support both flags and interactive prompts
   - Validate arguments before operations

4. **Filter Layer**
   - Create `filters.py` for query logic
   - Support multiple filter criteria
   - Implement sort strategies

---

## Component Design

### **1. Enhanced Models (src/models.py)**

#### **Task Dataclass**
```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Task:
    """Enhanced task with rich metadata."""

    # Core fields
    id: int
    title: str
    description: str = ""
    completed: bool = False

    # Metadata
    priority: str = "Medium"  # High, Medium, Low
    tags: list[str] = field(default_factory=list)
    due_date: datetime | None = None

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None

    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if self.due_date and not self.completed:
            return datetime.now() > self.due_date
        return False

    def time_to_complete(self) -> str | None:
        """Calculate time taken to complete task."""
        if self.completed_at:
            delta = self.completed_at - self.created_at
            return format_duration(delta)
        return None
```

#### **Config Dataclass**
```python
@dataclass
class Config:
    """User configuration settings."""
    default_priority: str = "Medium"
    list_view: str = "default"  # default, compact, detailed
    auto_save: bool = True
    confirm_delete: bool = True
    data_file: str = ".todo-data.json"
    config_file: str = ".todo-config.json"
```

---

### **2. Enhanced Validators (src/validators.py)**

#### **New Validation Functions**
```python
def validate_priority(priority: str) -> str | None:
    """Validate priority level."""
    valid = ["high", "medium", "low"]
    if priority.lower() not in valid:
        return "Priority must be High, Medium, or Low"
    return None

def validate_tags(tags: list[str]) -> str | None:
    """Validate tag list."""
    if len(tags) > 10:
        return "Maximum 10 tags per task"

    for tag in tags:
        if not re.match(r'^[a-zA-Z0-9_-]+$', tag):
            return f"Invalid tag '{tag}': Use only letters, numbers, -, _"
        if len(tag) > 20:
            return f"Tag '{tag}' too long (max 20 characters)"

    return None

def parse_due_date(date_str: str) -> datetime | None:
    """Parse due date from various formats."""
    # ISO format: 2026-01-15
    # Relative: tomorrow, next week, in 3 days
    # Short: 01/15, 15-01
    # Returns datetime or None if invalid
    pass

def validate_search_keyword(keyword: str) -> str | None:
    """Validate search keyword."""
    if len(keyword) < 2:
        return "Search keyword must be at least 2 characters"
    return None
```

---

### **3. Persistence Layer (src/persistence.py) - NEW**

#### **Responsibilities**
- Load tasks from JSON on startup
- Save tasks after every operation
- Handle file corruption
- Atomic writes to prevent data loss
- Config file management

#### **Implementation**
```python
import json
from pathlib import Path
from typing import List
from src.models import Task, Config

class DataStore:
    """Manages JSON persistence for tasks and config."""

    def __init__(self, data_file: str = ".todo-data.json"):
        self.data_file = Path(data_file)
        self.backup_file = Path(f"{data_file}.backup")

    def load_tasks(self) -> List[Task]:
        """Load tasks from JSON file."""
        if not self.data_file.exists():
            return []

        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return [Task(**task_dict) for task_dict in data]
        except (json.JSONDecodeError, KeyError) as e:
            # Corrupted file - restore from backup
            console.print(f"⚠️ Data file corrupted, restoring from backup...")
            return self._restore_from_backup()

    def save_tasks(self, tasks: List[Task]) -> None:
        """Save tasks to JSON with atomic write."""
        # Backup current file
        if self.data_file.exists():
            self.data_file.rename(self.backup_file)

        # Write new data
        try:
            data = [asdict(task) for task in tasks]
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            # Restore backup on failure
            if self.backup_file.exists():
                self.backup_file.rename(self.data_file)
            raise

    def load_config(self) -> Config:
        """Load user configuration."""
        # Similar to load_tasks
        pass

    def save_config(self, config: Config) -> None:
        """Save user configuration."""
        # Similar to save_tasks
        pass
```

---

### **4. Enhanced Operations (src/operations.py)**

#### **TaskManager Extensions**
```python
class TaskManager:
    """Enhanced task manager with advanced operations."""

    def __init__(self, data_store: DataStore):
        self.tasks: list[Task] = data_store.load_tasks()
        self.next_id: int = self._calculate_next_id()
        self.data_store = data_store

    def add(
        self,
        title: str,
        description: str = "",
        priority: str = "Medium",
        tags: list[str] | None = None,
        due_date: datetime | None = None
    ) -> Task:
        """Add task with enhanced metadata."""
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags or [],
            due_date=due_date,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.tasks.append(task)
        self.next_id += 1
        self._auto_save()
        return task

    def update(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        priority: str | None = None,
        tags: list[str] | None = None,
        due_date: datetime | None = None
    ) -> Task | None:
        """Update task with partial field updates."""
        task = self.get_by_id(task_id)
        if task is None:
            return None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority is not None:
            task.priority = priority
        if tags is not None:
            task.tags = tags
        if due_date is not None:
            task.due_date = due_date

        task.updated_at = datetime.now()
        self._auto_save()
        return task

    def complete_multiple(self, task_ids: list[int]) -> int:
        """Complete multiple tasks. Returns count."""
        count = 0
        for task_id in task_ids:
            task = self.toggle_complete(task_id)
            if task and task.completed:
                count += 1
        return count

    def complete_all(self) -> int:
        """Complete all incomplete tasks. Returns count."""
        count = 0
        for task in self.tasks:
            if not task.completed:
                task.completed = True
                task.completed_at = datetime.now()
                count += 1
        self._auto_save()
        return count

    def delete_multiple(self, task_ids: list[int]) -> int:
        """Delete multiple tasks. Returns count."""
        count = 0
        for task_id in task_ids:
            if self.delete(task_id):
                count += 1
        return count

    def delete_completed(self) -> int:
        """Delete all completed tasks. Returns count."""
        completed = [t for t in self.tasks if t.completed]
        count = len(completed)
        self.tasks = [t for t in self.tasks if not t.completed]
        self._auto_save()
        return count

    def get_statistics(self) -> dict:
        """Calculate task statistics."""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t.completed])
        incomplete = total - completed

        # Priority breakdown
        high = len([t for t in self.tasks if t.priority == "High"])
        medium = len([t for t in self.tasks if t.priority == "Medium"])
        low = len([t for t in self.tasks if t.priority == "Low"])

        # Overdue count
        overdue = len([t for t in self.tasks if t.is_overdue()])

        # Completion rate
        rate = (completed / total * 100) if total > 0 else 0

        return {
            "total": total,
            "completed": completed,
            "incomplete": incomplete,
            "completion_rate": rate,
            "by_priority": {"High": high, "Medium": medium, "Low": low},
            "overdue": overdue
        }

    def _auto_save(self) -> None:
        """Auto-save tasks if enabled."""
        if config.auto_save:
            self.data_store.save_tasks(self.tasks)
```

---

### **5. Filter Layer (src/filters.py) - NEW**

#### **Responsibilities**
- Filter tasks by status, priority, tags
- Sort tasks by various fields
- Search tasks by keyword

#### **Implementation**
```python
from typing import List, Callable
from src.models import Task

def filter_by_status(tasks: List[Task], status: str) -> List[Task]:
    """Filter tasks by completion status."""
    if status == "complete":
        return [t for t in tasks if t.completed]
    elif status == "incomplete":
        return [t for t in tasks if not t.completed]
    else:  # all
        return tasks

def filter_by_priority(tasks: List[Task], priority: str) -> List[Task]:
    """Filter tasks by priority level."""
    return [t for t in tasks if t.priority.lower() == priority.lower()]

def filter_by_tag(tasks: List[Task], tag: str) -> List[Task]:
    """Filter tasks containing the specified tag."""
    return [t for t in tasks if tag.lower() in [t.lower() for t in t.tags]]

def filter_by_tags_any(tasks: List[Task], tags: List[str]) -> List[Task]:
    """Filter tasks containing ANY of the specified tags (OR logic)."""
    tag_set = set(tag.lower() for tag in tags)
    return [t for t in tasks if any(t_tag.lower() in tag_set for t_tag in t.tags)]

def search_tasks(tasks: List[Task], keyword: str) -> List[Task]:
    """Search tasks by keyword in title or description."""
    keyword_lower = keyword.lower()
    return [
        t for t in tasks
        if keyword_lower in t.title.lower() or keyword_lower in t.description.lower()
    ]

def sort_tasks(
    tasks: List[Task],
    sort_by: str,
    reverse: bool = False
) -> List[Task]:
    """Sort tasks by specified field."""

    sort_keys: dict[str, Callable] = {
        "id": lambda t: t.id,
        "title": lambda t: t.title.lower(),
        "priority": lambda t: _priority_sort_key(t.priority),
        "created": lambda t: t.created_at,
        "due": lambda t: t.due_date or datetime.max,
    }

    key_func = sort_keys.get(sort_by, lambda t: t.id)
    return sorted(tasks, key=key_func, reverse=reverse)

def _priority_sort_key(priority: str) -> int:
    """Convert priority to sort key (High=0, Medium=1, Low=2)."""
    return {"High": 0, "Medium": 1, "Low": 2}.get(priority, 3)
```

---

### **6. Command Parser (src/parsers.py) - NEW**

#### **Responsibilities**
- Parse command-line flags for each command
- Support both flags and interactive prompts
- Validate arguments

#### **Implementation**
```python
import argparse
from typing import Tuple, Dict, Any

class CommandParser:
    """Parse command-line arguments for enhanced commands."""

    @staticmethod
    def parse_add_args(args: List[str]) -> Dict[str, Any]:
        """Parse /add command arguments."""
        parser = argparse.ArgumentParser(prog='/add', add_help=False)
        parser.add_argument('-t', '--title', type=str)
        parser.add_argument('-d', '--description', type=str, default="")
        parser.add_argument('-p', '--priority', type=str, default="Medium")
        parser.add_argument('--tags', type=str)  # Comma-separated
        parser.add_argument('--due', type=str)

        try:
            parsed = parser.parse_args(args)
            return {
                'title': parsed.title,
                'description': parsed.description,
                'priority': parsed.priority,
                'tags': parsed.tags.split(',') if parsed.tags else [],
                'due': parsed.due
            }
        except SystemExit:
            return None  # Invalid args

    @staticmethod
    def parse_list_args(args: List[str]) -> Dict[str, Any]:
        """Parse /list command arguments."""
        parser = argparse.ArgumentParser(prog='/list', add_help=False)
        parser.add_argument('-s', '--status', type=str, default="all")
        parser.add_argument('-p', '--priority', type=str)
        parser.add_argument('--tag', type=str)
        parser.add_argument('--sort', type=str, default="id")
        parser.add_argument('--reverse', action='store_true')
        parser.add_argument('--compact', action='store_true')
        parser.add_argument('--detailed', action='store_true')

        try:
            parsed = parser.parse_args(args)
            return vars(parsed)
        except SystemExit:
            return None

    # Similar methods for update, complete, delete
```

---

### **7. Formatters (src/formatters.py) - NEW**

#### **Responsibilities**
- Rich formatting utilities
- Table generation
- Panel creation
- Chart rendering

#### **Implementation**
```python
from rich.table import Table
from rich.panel import Panel
from rich.progress import BarColumn, Progress
from rich import box

def create_task_table(
    tasks: List[Task],
    view_mode: str = "default"
) -> Table:
    """Create Rich table for task list."""

    if view_mode == "compact":
        table = Table(box=box.SIMPLE, show_header=True)
        table.add_column("ID", style="cyan", width=5)
        table.add_column("Status", width=8)
        table.add_column("Title", style="yellow")

    elif view_mode == "detailed":
        table = Table(box=box.ROUNDED, show_header=True)
        table.add_column("ID", style="cyan", width=5)
        table.add_column("Status", width=8)
        table.add_column("Priority", width=10)
        table.add_column("Title", style="yellow", width=25)
        table.add_column("Description", width=30)
        table.add_column("Tags", style="magenta", width=15)
        table.add_column("Due", style="red", width=12)

    else:  # default
        table = Table(
            title="📋 [bold cyan]Your Tasks[/bold cyan]",
            box=box.ROUNDED,
            show_header=True,
            border_style="cyan"
        )
        table.add_column("ID", style="cyan", width=5)
        table.add_column("Status", width=8)
        table.add_column("Priority", width=10)
        table.add_column("Title", style="yellow", width=30)
        table.add_column("Description", width=40)

    for task in tasks:
        # Format status
        status = "[green]✅[/green]" if task.completed else "[red]❌[/red]"

        # Format priority with color
        priority_colors = {"High": "red", "Medium": "yellow", "Low": "green"}
        priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        p_color = priority_colors.get(task.priority, "white")
        p_emoji = priority_emoji.get(task.priority, "⚪")
        priority_display = f"[{p_color}]{p_emoji} {task.priority}[/{p_color}]"

        # Add row based on view mode
        if view_mode == "compact":
            table.add_row(str(task.id), status, task.title)
        elif view_mode == "detailed":
            tags_str = ", ".join(task.tags) if task.tags else "-"
            due_str = format_due_date(task.due_date, task.is_overdue())
            table.add_row(
                str(task.id), status, priority_display,
                task.title, task.description[:30], tags_str, due_str
            )
        else:
            table.add_row(
                str(task.id), status, priority_display,
                task.title[:30], task.description[:40]
            )

    return table

def create_stats_panel(stats: dict) -> Panel:
    """Create statistics dashboard panel."""
    content = f"""
    📊 [bold cyan]Task Statistics[/bold cyan]

    Total Tasks: {stats['total']}
    Completed: [green]{stats['completed']}[/green]
    Incomplete: [yellow]{stats['incomplete']}[/yellow]
    Completion Rate: [cyan]{stats['completion_rate']:.1f}%[/cyan]

    [bold]By Priority:[/bold]
    🔴 High: {stats['by_priority']['High']}
    🟡 Medium: {stats['by_priority']['Medium']}
    🟢 Low: {stats['by_priority']['Low']}

    {'⚠️  [red]Overdue: ' + str(stats['overdue']) + '[/red]' if stats['overdue'] > 0 else '✅ No overdue tasks'}
    """

    return Panel.fit(content, border_style="cyan", padding=(1, 2))

def create_task_detail_panel(task: Task) -> Panel:
    """Create detailed task view panel."""
    content = f"""
    [bold cyan]Task #{task.id}[/bold cyan]

    Title: {task.title}
    Description: {task.description or "(none)"}

    Status: {"[green]✅ Complete[/green]" if task.completed else "[red]❌ Incomplete[/red]"}
    Priority: {format_priority(task.priority)}
    Tags: {', '.join(task.tags) if task.tags else "(none)"}
    Due: {format_due_date(task.due_date, task.is_overdue())}

    Created: {format_relative_time(task.created_at)}
    Updated: {format_relative_time(task.updated_at)}
    {f"Completed: {format_relative_time(task.completed_at)}" if task.completed_at else ""}
    {f"Time to complete: {task.time_to_complete()}" if task.completed else ""}

    {f"[red]⚠️  OVERDUE by {format_overdue_delta(task.due_date)}[/red]" if task.is_overdue() else ""}
    """

    return Panel.fit(content, border_style="cyan", padding=(1, 2))
```

---

## Implementation Phases

### **Phase 1: Data Model & Persistence (3 hours)**
1. Enhance `Task` dataclass with new fields
2. Create `Config` dataclass
3. Implement `persistence.py` (DataStore class)
4. Add auto-save/load logic
5. Test JSON serialization with datetime fields

**Deliverable:** Tasks persist across app restarts

---

### **Phase 2: Enhanced Validators (1 hour)**
1. Add `validate_priority()`
2. Add `validate_tags()`
3. Add `parse_due_date()` with multiple formats
4. Add `validate_search_keyword()`

**Deliverable:** All new fields validated

---

### **Phase 3: Filter & Search (2 hours)**
1. Create `filters.py` module
2. Implement filter functions (status, priority, tags)
3. Implement `search_tasks()`
4. Implement `sort_tasks()` with multiple strategies

**Deliverable:** `/list --status incomplete --sort priority` works

---

### **Phase 4: Command Parser (2 hours)**
1. Create `parsers.py` module
2. Implement `parse_add_args()`
3. Implement `parse_list_args()`
4. Implement `parse_update_args()`
5. Handle parsing errors gracefully

**Deliverable:** `/add -t "Task" -p high` works

---

### **Phase 5: Enhanced Operations (2 hours)**
1. Update `TaskManager.add()` with new parameters
2. Update `TaskManager.update()` for partial updates
3. Add `complete_multiple()` and `complete_all()`
4. Add `delete_multiple()` and `delete_completed()`
5. Add `get_statistics()`

**Deliverable:** All bulk operations work

---

### **Phase 6: Rich Formatters (1.5 hours)**
1. Create `formatters.py` module
2. Implement `create_task_table()` with view modes
3. Implement `create_stats_panel()`
4. Implement `create_task_detail_panel()`
5. Add helper functions (format_due_date, format_priority, etc.)

**Deliverable:** Beautiful, rich output for all commands

---

### **Phase 7: Enhanced CLI Commands (3 hours)**
1. Update `/add` with flag support
2. Update `/list` with filters, sort, view modes
3. Update `/update` with flag support
4. Update `/complete` for bulk operations
5. Update `/delete` for bulk operations
6. Add `/search` command
7. Add `/show` command
8. Add `/stats` command
9. Add `/export` command
10. Add `/config` command
11. Add command aliases

**Deliverable:** All enhanced commands functional

---

### **Phase 8: Testing & Polish (1.5 hours)**
1. Manual test all commands
2. Test edge cases (empty list, invalid inputs)
3. Test file corruption recovery
4. Test with 100+ tasks for performance
5. Update help documentation

**Deliverable:** Production-ready app

---

## Risk Analysis

### **High Risk**

#### **R1: Datetime Serialization in JSON**
- **Issue:** Python datetime objects not JSON-serializable by default
- **Mitigation:** Use `json.dump(default=str)` and parse back on load
- **Contingency:** Store as ISO format strings

#### **R2: File Corruption**
- **Issue:** JSON file could be corrupted, losing all data
- **Mitigation:** Implement atomic writes with backup file
- **Contingency:** Keep `.backup` file, restore on corruption

### **Medium Risk**

#### **R3: Performance with Large Task Lists**
- **Issue:** Loading/saving 1000+ tasks could be slow
- **Mitigation:** Profile with large datasets, optimize if needed
- **Contingency:** Add lazy loading or pagination

#### **R4: Command Parsing Complexity**
- **Issue:** argparse in interactive CLI can be tricky
- **Mitigation:** Catch SystemExit, provide clear error messages
- **Contingency:** Fall back to interactive prompts on parse failure

### **Low Risk**

#### **R5: Due Date Parsing**
- **Issue:** Relative dates ("tomorrow", "next week") can be ambiguous
- **Mitigation:** Support common formats only, show examples in errors
- **Contingency:** Require ISO format if parsing fails

#### **R6: Backward Compatibility**
- **Issue:** Old JSON files won't have new fields
- **Mitigation:** Use dataclass defaults for missing fields
- **Contingency:** Provide migration script if needed

---

## Testing Strategy

### **Unit Tests**
```python
# test_validators.py
def test_validate_priority():
    assert validate_priority("High") is None
    assert validate_priority("Invalid") is not None

# test_filters.py
def test_filter_by_priority():
    tasks = [Task(id=1, priority="High"), Task(id=2, priority="Low")]
    result = filter_by_priority(tasks, "High")
    assert len(result) == 1

# test_persistence.py
def test_save_load_tasks():
    store = DataStore(".test-data.json")
    tasks = [Task(id=1, title="Test")]
    store.save_tasks(tasks)
    loaded = store.load_tasks()
    assert len(loaded) == 1
    assert loaded[0].title == "Test"
```

### **Integration Tests**
```python
def test_add_with_metadata():
    manager = TaskManager(data_store)
    task = manager.add("Test", priority="High", tags=["urgent"])
    assert task.priority == "High"
    assert "urgent" in task.tags

def test_filter_and_sort():
    # Add 10 tasks with mixed priorities
    # Filter by incomplete + sort by priority
    # Verify order: High → Medium → Low
```

### **Manual Test Scenarios**
1. **Empty State:** Start fresh, verify welcome message
2. **Basic CRUD:** Add, list, update, complete, delete
3. **Flag Commands:** Test all `/add -t "..."` variations
4. **Filters:** Test all filter combinations
5. **Search:** Test keyword matching and highlighting
6. **Bulk Ops:** Test complete-all, delete-completed
7. **Statistics:** Verify counts and percentages
8. **Export:** Export and verify JSON/CSV/MD formats
9. **Persistence:** Add tasks, exit, restart, verify loaded
10. **Corruption:** Corrupt JSON file, verify recovery

---

## Performance Targets

| Operation | Target | Current |
|-----------|--------|---------|
| App startup (100 tasks) | < 1s | TBD |
| Add task | < 50ms | ~5ms |
| List all tasks (100) | < 100ms | TBD |
| Filter + sort (100) | < 150ms | TBD |
| Search (100 tasks) | < 200ms | TBD |
| Save to JSON (100) | < 500ms | TBD |
| Export CSV (100) | < 1s | TBD |

---

## Backward Compatibility

### **Existing JSON Files**
Old task format:
```json
{
  "id": 1,
  "title": "Task",
  "description": "Desc",
  "completed": false
}
```

New format adds fields with defaults:
```json
{
  "id": 1,
  "title": "Task",
  "description": "Desc",
  "completed": false,
  "priority": "Medium",
  "tags": [],
  "due_date": null,
  "created_at": "2026-01-05T10:00:00",
  "updated_at": "2026-01-05T10:00:00",
  "completed_at": null
}
```

**Migration:** Dataclass defaults handle missing fields automatically.

---

## Code Quality Standards

### **Type Hints**
- All functions must have type hints
- Use `str | None` (not `Optional[str]`)
- Use `list[Task]` (not `List[Task]`)

### **Docstrings**
- All public functions have docstrings
- Format: Google-style
- Include Args, Returns, Examples

### **Error Handling**
- Validate inputs before operations
- Return `None` for not found (not exceptions)
- Use Rich panels for error messages
- Never let app crash on bad input

### **Formatting**
- Use Rich for all console output
- Consistent emoji usage
- Color scheme: green=success, red=error, yellow=warning, cyan=info

---

## Demo Preparation

### **Demo Data Setup Script**
```python
# demo_setup.py
def create_demo_data():
    """Create realistic demo data."""
    manager = TaskManager(data_store)

    # High priority tasks
    manager.add("Fix authentication bug", "JWT validation issue",
                priority="High", tags=["bug", "security", "urgent"])

    manager.add("Deploy to production", "Use blue-green deployment",
                priority="High", tags=["deployment", "ops"],
                due_date=parse_due_date("tomorrow"))

    # Medium priority
    manager.add("Write API documentation", "OpenAPI specs for v2",
                priority="Medium", tags=["docs", "api"])

    # Completed tasks
    task = manager.add("Setup CI/CD pipeline", priority="Medium",
                       tags=["devops"])
    manager.toggle_complete(task.id)

    # Low priority
    manager.add("Refactor utils module", priority="Low",
                tags=["refactor", "tech-debt"])
```

---

## Success Criteria

### **Must Pass**
- ✅ All existing features work unchanged
- ✅ JSON persistence functional
- ✅ All filters work correctly
- ✅ Search returns accurate results
- ✅ Statistics are accurate
- ✅ Export formats valid
- ✅ No crashes on invalid input
- ✅ Help documentation complete

### **Performance**
- ✅ Startup < 1s with 100 tasks
- ✅ All operations < 500ms

### **Quality**
- ✅ Type hints on all functions
- ✅ Docstrings on all public functions
- ✅ No linting errors

---

## Next Steps

1. ✅ Spec approved
2. ✅ Plan reviewed
3. ⏳ Generate task breakdown (tasks.md)
4. ⏳ Begin Phase 1 implementation
5. ⏳ Incremental testing
6. ⏳ Demo preparation

---

**Status:** Ready for Task Breakdown
**Last Updated:** 2026-01-05
