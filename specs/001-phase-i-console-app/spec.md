# Feature Specification: Phase I - Todo In-Memory Python Console App

**Feature Branch**: `001-phase-i-console-app`
**Created**: 2025-12-31
**Status**: Draft
**Input**: User description: "Phase I: Todo In-Memory Python Console App - Build a command-line todo application that stores tasks in memory using Python 3.13+, demonstrating mastery of spec-driven development workflow with Claude Code and Spec-Kit Plus."

## Project Context

This is Phase I of a 5-phase hackathon project 'Evolution of Todo' where we progressively build from a simple CLI app to a cloud-native AI system. This phase establishes the foundation.

**Target Audience**: Developers learning spec-driven development and AI-native software architecture

**Objective**: Build a command-line todo application that stores tasks in memory (no database) using Python 3.13+, demonstrating mastery of spec-driven development workflow with Claude Code and Spec-Kit Plus.

## Clarifications

### Session 2025-12-31

- Q: CLI interaction pattern - should the application use an interactive menu with numbered options or a command-based interface with slash prefix commands? → A: Command-based with slash prefix (/add, /list, /update, /delete, /complete, /exit)
- Q: Input method - should commands accept inline arguments or use interactive prompts for input collection? → A: Prompted inputs (e.g., `/add` → prompts for title → prompts for description)
- Q: Data structure - should tasks be stored as List[Dict], List[Task] dataclass, or custom TaskManager class? → A: List[Task] dataclass with @dataclass decorator
- Q: Project structure - should the code be organized in a single main.py file or modular files? → A: Modular structure with separate models.py, cli.py, and main.py files
- Q: Whitespace handling - should the system trim whitespace from titles and reject whitespace-only inputs? → A: Trim leading/trailing whitespace, then reject if empty or whitespace-only

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create and View Tasks (Priority: P1)

As a developer, I want to add tasks to my todo list and view them so that I can track my work items during a coding session.

**Why this priority**: This is the core MVP functionality. Without the ability to create and view tasks, the application has no value.

**Independent Test**: Can be fully tested by adding multiple tasks with varying titles and descriptions, then viewing the complete list. Delivers immediate value as a basic task tracker.

**Acceptance Scenarios**:

1. **Given** an empty task list, **When** I add a task with title "Fix login bug" and description "Update JWT validation", **Then** I see confirmation with task ID 1
2. **Given** a task list with 2 tasks, **When** I view the task list, **Then** I see all tasks displayed with ID, title, status, and description preview
3. **Given** an empty task list, **When** I view the task list, **Then** I see message "No tasks yet. Add one with /add"

---

### User Story 2 - Mark Task Completion (Priority: P2)

As a developer, I want to mark tasks as complete or incomplete so that I can track my progress.

**Why this priority**: Completion tracking is essential for a todo app to be useful. This builds on P1 by adding state management.

**Independent Test**: Can be tested by creating tasks, marking some complete, viewing the list to verify status indicators, then toggling back to incomplete.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 marked incomplete, **When** I mark it complete, **Then** status changes to ✓ Complete
2. **Given** a task with ID 2 marked complete, **When** I mark it incomplete, **Then** status changes to ✗ Incomplete
3. **Given** an invalid task ID 99, **When** I try to mark it complete, **Then** I see error "Task #99 not found"

---

### User Story 3 - Update Task Details (Priority: P3)

As a developer, I want to update task titles and descriptions so that I can correct mistakes or add more information.

**Why this priority**: Updates are important but not critical for MVP. Users can delete and recreate if needed as a workaround.

**Independent Test**: Can be tested by creating a task, updating just the title, then updating just the description, then updating both simultaneously.

**Acceptance Scenarios**:

1. **Given** a task with ID 1, **When** I update only the title to "Deploy to production", **Then** title changes and description remains unchanged
2. **Given** a task with ID 1, **When** I update only the description to "Use blue-green deployment", **Then** description changes and title remains unchanged
3. **Given** task ID 99 doesn't exist, **When** I try to update it, **Then** I see error "Task #99 not found"

---

### User Story 4 - Delete Tasks (Priority: P4)

As a developer, I want to delete tasks I no longer need so that my list stays relevant.

**Why this priority**: Deletion is a cleanup operation. While useful, it's the lowest priority feature for a working todo app.

**Independent Test**: Can be tested by creating tasks, deleting specific ones, and verifying they no longer appear in the list.

**Acceptance Scenarios**:

1. **Given** a task with ID 3, **When** I delete it after confirmation, **Then** task is removed and confirmation message shown
2. **Given** task ID 99 doesn't exist, **When** I try to delete it, **Then** I see error "Task #99 not found"
3. **Given** a delete command for task ID 5, **When** I decline the confirmation, **Then** task remains in the list

---

### Edge Cases

- What happens when user provides empty title? → Reject with error "Title cannot be empty"
- What happens when title exceeds 200 characters? → Reject with error "Title must be 1-200 characters"
- What happens when description exceeds 1000 characters? → Reject with error "Description must be 0-1000 characters"
- What happens when user provides only whitespace as title? → Trim whitespace first, then reject with error "Title cannot be empty"
- What happens when title has leading/trailing spaces? → Automatically trim before validation and storage
- What happens when task list has 100+ tasks? → Display all (performance not a concern for in-memory Phase I)
- What happens when user enters invalid command? → Show error and help text
- How does user exit the program? → [NEEDS CLARIFICATION: /exit, /quit, Ctrl+C, or all three?]

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create tasks with a title (1-200 characters, required) and description (0-1000 characters, optional)
- **FR-002**: System MUST auto-generate sequential integer IDs starting from 1 for each new task
- **FR-003**: System MUST display all tasks with ID, title, completion status, and description preview (first 50 characters)
- **FR-004**: System MUST allow users to toggle task completion status by ID
- **FR-005**: System MUST allow users to update task title and/or description by ID
- **FR-006**: System MUST allow users to delete tasks by ID after confirmation
- **FR-007**: System MUST show error message "Task #X not found" for invalid task IDs
- **FR-008**: System MUST validate title length (1-200 chars) and description length (0-1000 chars) after trimming whitespace
- **FR-013**: System MUST trim leading and trailing whitespace from title and description inputs before validation and storage
- **FR-009**: System MUST display friendly message "No tasks yet. Add one with /add" for empty task list
- **FR-010**: System MUST persist tasks in memory during program runtime only (no file/database persistence)
- **FR-011**: System MUST support command-based interface with slash prefix commands: /add, /list, /update, /delete, /complete, /exit
- **FR-012**: System MUST use interactive prompts for all input collection (commands trigger prompts for required/optional fields)

### Key Entities

- **Task**: Represents a todo item implemented as a Python dataclass with the following attributes:
  - `id`: int - Unique integer identifier (auto-generated, sequential)
  - `title`: str - Short description (1-200 characters, required)
  - `description`: str - Detailed notes (0-1000 characters, optional, default: "")
  - `completed`: bool - Completion status (default: False)
  - Implementation: Use @dataclass decorator from dataclasses module
  - Relationships: None (standalone entity in Phase I)

### Data Model Constraints

- **Task ID**: Auto-increment starting from 1, unique within session
- **Task ID Persistence**: Reset to 1 each program run (in-memory counter, not persisted)
- **Empty Description**: Allow empty string (description is optional, defaults to "")
- **Whitespace Handling**: Trim leading/trailing whitespace from all text inputs; reject title if empty or whitespace-only after trimming

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 5 core features (add, view, update, delete, toggle completion) are fully functional via CLI
- **SC-002**: User can complete a full task lifecycle (create → view → update → mark complete → delete) in under 60 seconds
- **SC-003**: System handles invalid inputs gracefully with clear error messages (no crashes or stack traces visible to user)
- **SC-004**: Code is generated 100% via Claude Code from specifications (zero manual coding)
- **SC-005**: All error conditions return user-friendly messages matching specified format ("Task #X not found")
- **SC-006**: Task data persists for the entire program runtime (not lost between commands)
- **SC-007**: [NEEDS CLARIFICATION: Code quality standard - teaching demo with extensive comments or production-quality minimal comments?]

### Quality Attributes

- **Code Style**: [NEEDS CLARIFICATION: PEP 8 compliance? Specific naming conventions? Max function length?]
- **Type Hints**: [NEEDS CLARIFICATION: Python 3.13 new syntax or typing module for compatibility?]
- **Error Handling**: [NEEDS CLARIFICATION: Try-except blocks? Validation functions? Custom exceptions?]
- **CLI UX**: [NEEDS CLARIFICATION: Color coding? Command shortcuts? Specific help text format?]

## Technical Constraints

### Technology Stack (Immutable per Constitution)

- **Language**: Python 3.13+
- **Package Manager**: UV
- **Libraries**: Standard library only (dataclasses, typing, etc.)
- **No External Dependencies**: No database, no web framework, no third-party CLI libraries
- **Data Structure**: List[Task] where Task is a @dataclass with typed fields (id, title, description, completed)
- **Command Parsing**: [NEEDS CLARIFICATION: argparse library or manual string parsing?]

### Architecture Constraints

- **In-Memory Storage**: Python list containing Task dataclass instances (tasks: List[Task]), simple linear storage sufficient for Phase I
- **Project Structure**: Modular organization with separation of concerns:
  - `src/models.py` - Task dataclass definition and data model
  - `src/cli.py` - CLI interface, command parsing, user interaction
  - `src/main.py` - Entry point, application orchestration, task list management
- **No GUI**: Pure console interface, text-based interaction only
- **No Persistence**: Data lost when program exits (explicitly out of scope for Phase I)

## Out of Scope (Not Building in Phase I)

- Database or file persistence (comes in Phase II)
- Multi-user support (comes in Phase II)
- Web interface (comes in Phase II)
- AI chatbot (comes in Phase III)
- Cloud deployment (comes in Phase IV-V)
- Task prioritization, tags, due dates, reminders (comes in Phase V)
- Bulk operations (delete all, mark all complete) - [NEEDS CLARIFICATION: Strictly single-task ops?]
- Command history or undo functionality
- Task filtering or search (comes in Phase V)
- Data export/import
- Task sorting beyond ID ascending

## Deliverables

1. `/src` folder with modular Python source code:
   - `src/models.py` - Task dataclass definition
   - `src/cli.py` - CLI interface and command handling
   - `src/main.py` - Application entry point and orchestration
2. `/specs/001-phase-i-console-app/` folder with this specification file
3. `CLAUDE.md` with Claude Code instructions at repository root
4. `README.md` with setup and usage instructions
5. Constitution file at `.specify/memory/constitution.md` (already exists)

## UI/UX Specifications

### Display Formatting

- **Task List Format**: [NEEDS CLARIFICATION: Table? Bulleted list? Include creation timestamp?]
- **Status Indicators**: [NEEDS CLARIFICATION: ✓/✗ or [X]/[ ] or DONE/PENDING?]
- **Error Messages**: [NEEDS CLARIFICATION: Verbose explanations or terse error codes?]

### Interaction Pattern

- **CLI Style**: Command-based with slash prefix (/add, /list, /update, /delete, /complete, /exit)
- **Input Method**: Prompted inputs - commands trigger interactive prompts for required/optional fields (e.g., `/add` → prompt "Title:" → prompt "Description (optional):")
- **Exit Command**: [NEEDS CLARIFICATION: /exit, /quit, Ctrl+C, or multiple options?]
- **Delete Confirmation**: [NEEDS CLARIFICATION: Show task details before confirming? Support --force flag?]

## Development Workflow

This specification feeds into the Spec-Kit Plus workflow per the constitution:

1. ✅ `/sp.specify` → Create this specification (speckit.specify)
2. ⏭️ `/sp.clarify` → Resolve ambiguities and missing decisions
3. ⏭️ `/sp.plan` → Generate architecture and implementation approach (speckit.plan)
4. ⏭️ `/sp.tasks` → Break into atomic, testable work units (speckit.tasks)
5. ⏭️ `/sp.implement` → Claude Code generates code from tasks

## Compliance with Constitution

This specification aligns with the project constitution:

✅ **Spec-Driven Development**: This spec will drive all code generation via Claude Code
✅ **Phase I Requirements**: Covers all 5 Basic Level features (Add, View, Update, Delete, Mark Complete)
✅ **Technology Stack**: Python 3.13+, UV package manager as mandated
✅ **No Manual Coding**: All code will be generated from specs and tasks
✅ **Progressive Complexity**: Foundation for Phase II web app with persistence
✅ **Deliverables Match**: src/, specs/, CLAUDE.md, README.md as required

## Next Steps

**Before proceeding to planning**, the following clarifications are needed (marked with `[NEEDS CLARIFICATION]` above):

1. CLI interaction pattern (interactive menu vs command-based)
2. Input method (inline arguments vs prompted)
3. Data structure choice (List[Dict] vs dataclass vs TaskManager)
4. Project file structure (single main.py vs modular)
5. Code style standard (teaching demo vs production quality)
6. UI formatting details (status symbols, list format)
7. Whitespace handling in titles
8. Exit command options
9. Delete confirmation behavior
10. Error message verbosity

**Recommended next command**: `/sp.clarify` to resolve these ambiguities before architectural planning.
