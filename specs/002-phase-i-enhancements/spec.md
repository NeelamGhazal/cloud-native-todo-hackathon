# Phase I CLI Todo App - Enhancement Specification

**Feature ID:** 002-phase-i-enhancements
**Priority:** P1 (High)
**Status:** Draft
**Created:** 2026-01-05
**Author:** Product Architecture Team

---

## Executive Summary

Enhance the existing Phase I CLI Todo App with advanced features, improved UX, and richer data management while staying within Python CLI scope (no web, no database). Focus on making the app **demo-worthy** and **production-grade** with features that showcase technical depth.

---

## Problem Statement

### Current State
The Phase I app has solid CRUD operations but lacks:
- **Flexibility:** Limited options when creating/updating tasks
- **Filtering:** No way to view subsets of tasks
- **Sorting:** Tasks shown in insertion order only
- **Rich metadata:** Only basic title/description/status
- **Data persistence:** Tasks lost on app exit
- **Power features:** No bulk operations, search, or analytics

### Desired State
A **feature-rich CLI app** that demonstrates:
- Professional data management patterns
- Advanced querying and filtering
- Rich user interactions
- Persistent state management
- Business intelligence features
- LinkedIn demo-worthy polish

---

## User Stories

### **Epic 1: Enhanced Task Creation**

#### **US-1.1: Quick Add with Inline Parameters**
**As a** power user
**I want to** add tasks with all details in one command
**So that** I can quickly capture tasks without multiple prompts

**Acceptance Criteria:**
- ✅ Support `/add --title "Task" --desc "Details" --priority high`
- ✅ Support short flags: `-t`, `-d`, `-p`
- ✅ Fall back to interactive prompts if flags omitted
- ✅ Validate all inputs before creating task
- ✅ Show rich confirmation panel with all details

**Priority:** P1 (High/Medium/Low)

#### **US-1.2: Task Metadata with Priority and Tags**
**As a** organized user
**I want to** assign priority and tags to tasks
**So that** I can categorize and prioritize my work

**Acceptance Criteria:**
- ✅ Add `priority` field (High, Medium, Low)
- ✅ Add `tags` field (list of strings)
- ✅ Default priority to "Medium"
- ✅ Support multiple tags: `--tags "bug,urgent,backend"`
- ✅ Show priority with color coding (🔴 High, 🟡 Medium, 🟢 Low)

#### **US-1.3: Due Dates**
**As a** deadline-conscious user
**I want to** set due dates on tasks
**So that** I can track when work is due

**Acceptance Criteria:**
- ✅ Add `due_date` field (optional datetime)
- ✅ Support formats: `2026-01-15`, `tomorrow`, `next week`
- ✅ Show "⚠️ Overdue" indicator for past-due tasks
- ✅ Sort by due date in list view

---

### **Epic 2: Advanced Listing and Filtering**

#### **US-2.1: Filter Tasks by Status**
**As a** focused user
**I want to** view only complete or incomplete tasks
**So that** I can focus on relevant work

**Acceptance Criteria:**
- ✅ `/list --status complete` - Show only completed
- ✅ `/list --status incomplete` - Show only pending
- ✅ `/list --status all` - Show all (default)
- ✅ Short flag: `/list -s complete`

#### **US-2.2: Filter by Priority and Tags**
**As a** prioritized user
**I want to** filter tasks by priority or tags
**So that** I can focus on high-priority or specific categories

**Acceptance Criteria:**
- ✅ `/list --priority high` - Show only high-priority
- ✅ `/list --tag bug` - Show tasks tagged "bug"
- ✅ `/list --tag bug,urgent` - Show tasks with ANY listed tag (OR logic)
- ✅ Combine filters: `/list --priority high --status incomplete`

#### **US-2.3: Search Tasks**
**As a** user with many tasks
**I want to** search by keywords
**So that** I can quickly find specific tasks

**Acceptance Criteria:**
- ✅ `/search <keyword>` - Search in title and description
- ✅ Case-insensitive matching
- ✅ Highlight matched terms in results
- ✅ Show count: "Found 3 tasks matching 'bug'"

#### **US-2.4: Sort Tasks**
**As a** organized user
**I want to** sort tasks by different fields
**So that** I can view tasks in meaningful order

**Acceptance Criteria:**
- ✅ `/list --sort priority` - High → Low → tasks without priority
- ✅ `/list --sort due` - Soonest → latest → no due date
- ✅ `/list --sort created` - Newest → oldest
- ✅ `/list --sort title` - Alphabetical A→Z
- ✅ Default: sort by ID (insertion order)
- ✅ Support reverse: `--sort due --reverse`

#### **US-2.5: List View Modes**
**As a** user with varying detail needs
**I want to** choose between compact and detailed views
**So that** I can see appropriate information density

**Acceptance Criteria:**
- ✅ `/list` - Default table view (current)
- ✅ `/list --compact` - Minimal view (ID, status, title only)
- ✅ `/list --detailed` - Full view with all metadata
- ✅ Save preferred view mode in config

---

### **Epic 3: Enhanced Update Operations**

#### **US-3.1: Partial Updates with Flags**
**As a** efficient user
**I want to** update specific fields without prompts
**So that** I can make quick changes

**Acceptance Criteria:**
- ✅ `/update <id> --title "New title"`
- ✅ `/update <id> --priority high`
- ✅ `/update <id> --tags "new,tags"`
- ✅ `/update <id> --due 2026-01-20`
- ✅ Support multiple flags in one command
- ✅ Fall back to interactive mode if no flags

#### **US-3.2: Update Status Separately**
**As a** user tracking progress
**I want to** mark tasks complete or incomplete explicitly
**So that** I can manage task lifecycle

**Acceptance Criteria:**
- ✅ Keep `/complete <id>` for toggle behavior
- ✅ Add `/mark-complete <id>` - Always mark complete
- ✅ Add `/mark-incomplete <id>` - Always mark incomplete
- ✅ Show previous and new status in confirmation

---

### **Epic 4: Improved Complete and Delete**

#### **US-4.1: Bulk Complete Operations**
**As a** productive user
**I want to** complete multiple tasks at once
**So that** I can efficiently update status

**Acceptance Criteria:**
- ✅ `/complete-all` - Mark all incomplete tasks complete
- ✅ `/complete <id1> <id2> <id3>` - Complete multiple by ID
- ✅ `/complete --tag bug` - Complete all tasks with tag
- ✅ Show count: "Marked 5 tasks as complete"

#### **US-4.2: Bulk Delete with Safety**
**As a** cleanup-conscious user
**I want to** delete multiple tasks safely
**So that** I can maintain a clean task list

**Acceptance Criteria:**
- ✅ `/delete-completed` - Remove all completed tasks
- ✅ `/delete <id1> <id2> <id3>` - Delete multiple by ID
- ✅ Always require confirmation for bulk deletes
- ✅ Show preview: "About to delete 5 tasks"
- ✅ Support `--force` flag to skip confirmation (dangerous!)

#### **US-4.3: Improved Delete Feedback**
**As a** careful user
**I want to** see what I'm deleting before confirming
**So that** I don't accidentally remove important tasks

**Acceptance Criteria:**
- ✅ Show full task details in confirmation panel
- ✅ Use yellow warning panel (current behavior)
- ✅ Add "Type task title to confirm" for extra safety on important tasks
- ✅ Show success with task ID: "✅ Deleted task #5"

---

### **Epic 5: New Power Features**

#### **US-5.1: Statistics Dashboard**
**As a** data-driven user
**I want to** see task statistics and analytics
**So that** I can understand my productivity

**Acceptance Criteria:**
- ✅ `/stats` command shows:
  - Total tasks
  - Complete vs incomplete count
  - Completion rate percentage
  - Tasks by priority breakdown
  - Tasks by tag (top 5)
  - Overdue count
  - Today's completed count
- ✅ Display in beautiful panel with charts
- ✅ Use progress bars for visual representation

#### **US-5.2: Task History and Timestamps**
**As a** tracking-conscious user
**I want to** see when tasks were created/completed
**So that** I can track task lifecycle

**Acceptance Criteria:**
- ✅ Add `created_at` timestamp (datetime)
- ✅ Add `completed_at` timestamp (datetime or None)
- ✅ Add `updated_at` timestamp (datetime)
- ✅ Show in detailed view: "Created: 2 days ago"
- ✅ Show time elapsed: "Completed in 3 hours"

#### **US-5.3: Task Show (Detail View)**
**As a** detail-oriented user
**I want to** view full details of a single task
**So that** I can see all metadata clearly

**Acceptance Criteria:**
- ✅ `/show <id>` command
- ✅ Display in rich panel with all fields:
  - Title, description
  - Status, priority, tags
  - Created, updated, completed timestamps
  - Time tracking
- ✅ Show "⚠️ Overdue by 2 days" if applicable

#### **US-5.4: Export and Import**
**As a** data-portable user
**I want to** export and import task data
**So that** I can backup or share tasks

**Acceptance Criteria:**
- ✅ `/export json` - Save to `tasks-YYYY-MM-DD.json`
- ✅ `/export csv` - Save to `tasks-YYYY-MM-DD.csv`
- ✅ `/export md` - Save as Markdown checklist
- ✅ `/import <file>` - Load tasks from JSON file
- ✅ Prevent duplicate imports
- ✅ Show import summary: "Imported 10 tasks, skipped 2 duplicates"

#### **US-5.5: JSON Auto-Persistence**
**As a** user who values data
**I want to** have tasks automatically saved
**So that** I don't lose work on exit

**Acceptance Criteria:**
- ✅ Auto-save to `.todo-data.json` after every operation
- ✅ Auto-load on startup (silent if no file)
- ✅ Show notification on first load: "Loaded 5 tasks from previous session"
- ✅ Handle corrupted file gracefully (backup and start fresh)
- ✅ Use atomic writes to prevent data loss

#### **US-5.6: Configuration Management**
**As a** customization-loving user
**I want to** configure app preferences
**So that** I can personalize my experience

**Acceptance Criteria:**
- ✅ `/config` command to view all settings
- ✅ `/config set <key> <value>` to change settings
- ✅ Settings:
  - `default_priority` (High/Medium/Low)
  - `list_view` (default/compact/detailed)
  - `auto_save` (true/false)
  - `confirm_delete` (true/false)
- ✅ Save to `.todo-config.json`
- ✅ Show current value when viewing config

#### **US-5.7: Command Aliases and Shortcuts**
**As a** speed-focused user
**I want to** use short command names
**So that** I can work faster

**Acceptance Criteria:**
- ✅ `/a` = `/add`
- ✅ `/l` = `/list`
- ✅ `/u` = `/update`
- ✅ `/d` = `/delete`
- ✅ `/c` = `/complete`
- ✅ `/s` = `/search`
- ✅ `/h` = `/help`
- ✅ Show aliases in help table

---

## Success Criteria

### **Phase I Completion Requirements**

#### **Must Have (MVP+)**
- ✅ All existing functionality preserved
- ✅ Task metadata (priority, tags, timestamps)
- ✅ JSON auto-persistence
- ✅ Filter and sort capabilities
- ✅ Search functionality
- ✅ Statistics dashboard
- ✅ Command aliases

#### **Should Have**
- ✅ Due dates with overdue detection
- ✅ Bulk operations (complete-all, delete-completed)
- ✅ Export to JSON/CSV/Markdown
- ✅ Task detail view (`/show`)
- ✅ Config management

#### **Nice to Have**
- ✅ Import from JSON
- ✅ Multiple view modes (compact/detailed)
- ✅ Time tracking (task duration)
- ✅ Advanced filtering (combine filters)

---

## Constraints

### **Technical Constraints**
- ✅ Python 3.13+ standard library + Rich only
- ✅ No database (SQLite excluded in Phase I)
- ✅ No web frameworks
- ✅ No external APIs
- ✅ In-memory operations with JSON persistence
- ✅ Single-user, local CLI only

### **UX Constraints**
- ✅ All commands must remain intuitive
- ✅ Interactive prompts available for all operations
- ✅ Flag-based commands optional, not required
- ✅ Preserve existing command behavior as default
- ✅ Help documentation must be comprehensive

### **Performance Constraints**
- ✅ App startup < 1 second (even with 1000 tasks)
- ✅ All operations < 100ms response time
- ✅ Search across 1000 tasks < 200ms
- ✅ JSON save/load < 500ms

---

## Non-Goals (Out of Scope)

❌ **NOT in Phase I:**
- Database integration (Phase II)
- Web API or REST endpoints (Phase II)
- Multi-user support
- Cloud sync
- Mobile app
- Reminders or notifications
- Recurring tasks
- Subtasks or task hierarchy
- Calendar integration
- Team collaboration
- Authentication

---

## Data Model Changes

### **Enhanced Task Entity**

```python
@dataclass
class Task:
    """Enhanced task with rich metadata."""

    # Core fields (existing)
    id: int
    title: str
    description: str = ""
    completed: bool = False

    # New metadata fields
    priority: str = "Medium"  # High, Medium, Low
    tags: list[str] = field(default_factory=list)
    due_date: datetime | None = None

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None
```

### **Config Entity (New)**

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

## Validation Rules

### **Priority Field**
- Must be one of: "High", "Medium", "Low"
- Case-insensitive input (normalize to title case)
- Default: "Medium"

### **Tags Field**
- Each tag: 1-20 characters
- Alphanumeric + hyphens/underscores only
- Max 10 tags per task
- Case-insensitive matching
- Store as lowercase

### **Due Date Field**
- Optional (None allowed)
- Parse formats:
  - ISO: `2026-01-15`
  - Relative: `tomorrow`, `next week`, `in 3 days`
  - Short: `01/15`, `15-01`
- Must be future or today (warning if past)

### **Search Keywords**
- Min 2 characters
- Case-insensitive
- Match in title OR description
- Highlight matches in results

---

## Command Reference

### **Enhanced Commands**

| Command | Description | Flags | Examples |
|---------|-------------|-------|----------|
| `/add` | Create task with options | `-t`, `-d`, `-p`, `--tags`, `--due` | `/add -t "Fix bug" -p high --tags "urgent,backend"` |
| `/list` | View tasks with filters | `-s`, `-p`, `--tag`, `--sort`, `--compact`, `--detailed` | `/list -s incomplete --sort priority` |
| `/update` | Update task fields | `-t`, `-d`, `-p`, `--tags`, `--due` | `/update 5 -p high --due tomorrow` |
| `/complete` | Toggle or bulk complete | `<ids>`, `--tag`, `--all` | `/complete 1 2 3` or `/complete-all` |
| `/delete` | Delete with confirmation | `<ids>`, `--completed`, `--force` | `/delete 5` or `/delete-completed` |

### **New Commands**

| Command | Description | Examples |
|---------|-------------|----------|
| `/search <keyword>` | Find tasks by keyword | `/search "authentication"` |
| `/show <id>` | View task details | `/show 5` |
| `/stats` | Show statistics dashboard | `/stats` |
| `/export <format>` | Export to JSON/CSV/MD | `/export json` |
| `/import <file>` | Import tasks from JSON | `/import backup.json` |
| `/config [set]` | View/update config | `/config set list_view compact` |
| `/mark-complete <id>` | Force mark complete | `/mark-complete 3` |
| `/mark-incomplete <id>` | Force mark incomplete | `/mark-incomplete 3` |
| `/complete-all` | Complete all incomplete | `/complete-all` |
| `/delete-completed` | Delete all completed | `/delete-completed` |

### **Aliases**

| Alias | Full Command |
|-------|--------------|
| `/a` | `/add` |
| `/l` | `/list` |
| `/u` | `/update` |
| `/d` | `/delete` |
| `/c` | `/complete` |
| `/s` | `/search` |
| `/h` | `/help` |

---

## Error Handling

### **Priority Errors**
- Invalid priority → "Priority must be High, Medium, or Low"
- Show examples in error message

### **Tag Errors**
- Invalid tag format → "Tags must be alphanumeric (a-z, 0-9, -, _)"
- Too many tags → "Maximum 10 tags per task"

### **Due Date Errors**
- Invalid format → "Invalid date format. Use YYYY-MM-DD, 'tomorrow', or 'next week'"
- Past date → Warning (not error): "⚠️ Due date is in the past"

### **Search Errors**
- Too short → "Search keyword must be at least 2 characters"
- No results → "No tasks found matching '<keyword>'"

### **Import Errors**
- File not found → "File not found: <path>"
- Invalid JSON → "Invalid JSON format in file"
- Corrupted data → "Could not parse tasks from file"

---

## Demo Script (60 seconds)

```bash
# 1. Show banner and load existing tasks (3s)
python -m src.main

# 2. Show stats (5s)
/stats

# 3. Add high-priority task (7s)
/add -t "Fix authentication bug" -d "Update JWT validation" -p high --tags "bug,urgent" --due tomorrow

# 4. Add medium task (5s)
/add -t "Write documentation" -p medium --tags "docs"

# 5. List with filter (5s)
/list -s incomplete --sort priority

# 6. Search (4s)
/search "auth"

# 7. Show detail (5s)
/show 1

# 8. Complete task (4s)
/complete 1

# 9. Updated list (4s)
/list

# 10. Stats dashboard (5s)
/stats

# 11. Export (4s)
/export json

# 12. Exit (3s)
/exit
```

---

## Acceptance Tests

### **Test Scenarios**

#### **T1: Task Creation with Metadata**
```
GIVEN empty task list
WHEN /add -t "Test" -p high --tags "test,demo" --due tomorrow
THEN task created with all metadata
AND displayed in confirmation panel
AND auto-saved to JSON
```

#### **T2: Filtering and Sorting**
```
GIVEN 10 tasks with mixed priorities
WHEN /list -s incomplete --sort priority
THEN shows only incomplete tasks
AND sorted High → Medium → Low
```

#### **T3: Search Functionality**
```
GIVEN 20 tasks
WHEN /search "bug"
THEN shows only tasks with "bug" in title or description
AND highlights matched term
AND shows count
```

#### **T4: Bulk Operations**
```
GIVEN 5 incomplete tasks
WHEN /complete-all
THEN all tasks marked complete
AND shows confirmation count
AND updated completion stats
```

#### **T5: Export and Import**
```
GIVEN 10 tasks
WHEN /export json
THEN file created with all task data
WHEN /import <file>
THEN tasks loaded
AND duplicates skipped
AND summary shown
```

#### **T6: Statistics Dashboard**
```
GIVEN 20 tasks (12 complete, 8 incomplete, 3 overdue)
WHEN /stats
THEN shows correct counts
AND completion rate
AND priority breakdown
AND overdue alert
```

---

## Open Questions

1. **Date Parsing:** Use `dateutil.parser` or implement custom parser?
   - Recommendation: Simple custom parser for common cases only

2. **Tag Autocomplete:** Should we suggest existing tags when adding?
   - Recommendation: Phase II feature (requires more complex input handling)

3. **Task IDs:** Keep auto-increment or use UUIDs for import safety?
   - Recommendation: Keep auto-increment, handle duplicates in import

4. **Color Themes:** Allow customization or keep fixed scheme?
   - Recommendation: Fixed for Phase I, configurable in Phase II

5. **Max Tasks:** Any limits for performance?
   - Recommendation: Test with 1000 tasks, no hard limit

---

## Success Metrics

### **Demo Quality**
- ✅ All operations < 100ms response time
- ✅ Zero errors during 60-second demo
- ✅ Visual polish on all outputs
- ✅ Clear feedback for every action

### **Feature Completeness**
- ✅ 100% of Must Have features implemented
- ✅ 80%+ of Should Have features implemented
- ✅ 50%+ of Nice to Have features implemented

### **Code Quality**
- ✅ All existing tests pass
- ✅ New features have test coverage
- ✅ Type hints on all new code
- ✅ Docstrings on all public functions

---

## Timeline Estimate

- **Specification Review:** 1 hour
- **Implementation:** 8-12 hours
- **Testing:** 2-3 hours
- **Documentation:** 1 hour
- **Demo Preparation:** 1 hour

**Total:** 13-18 hours

---

## Next Steps

1. ✅ Review and approve specification
2. ⏳ Create implementation plan (plan.md)
3. ⏳ Generate task breakdown (tasks.md)
4. ⏳ Begin implementation
5. ⏳ Test and validate
6. ⏳ Record demo

---

**Status:** Ready for Implementation Planning
**Last Updated:** 2026-01-05
