# Phase I Enhancements - Task Breakdown

**Feature:** 002-phase-i-enhancements
**Total Tasks:** 78
**Estimated:** 12-15 hours
**Created:** 2026-01-05

---

## Task Summary

| Phase | Tasks | Parallelizable | Est. Hours |
|-------|-------|----------------|------------|
| Phase 1: Data Model & Persistence | 12 | 8 (67%) | 3h |
| Phase 2: Enhanced Validators | 8 | 7 (88%) | 1h |
| Phase 3: Filter & Search | 10 | 9 (90%) | 2h |
| Phase 4: Command Parser | 9 | 6 (67%) | 2h |
| Phase 5: Enhanced Operations | 13 | 10 (77%) | 2h |
| Phase 6: Rich Formatters | 10 | 8 (80%) | 1.5h |
| Phase 7: Enhanced CLI | 13 | 3 (23%) | 3h |
| Phase 8: Testing & Polish | 3 | 1 (33%) | 1.5h |
| **Total** | **78** | **52 (67%)** | **16h** |

---

## Legend

- `[P]` = Parallelizable (can work on independently)
- `[BLOCKS]` = Blocks other tasks
- `[DEP: TX]` = Depends on task X
- `[US-X]` = Implements user story X

---

## Phase 1: Data Model & Persistence (3 hours)

### **T001-T012: Data Model & Persistence Setup**

- [ ] **T001** [P] [BLOCKS] Add `priority` field to Task dataclass in src/models.py
  - Type: `str = "Medium"`
  - Validation: High, Medium, Low only
  - Default: "Medium"

- [ ] **T002** [P] [BLOCKS] Add `tags` field to Task dataclass in src/models.py
  - Type: `list[str] = field(default_factory=list)`
  - Store as lowercase for consistency

- [ ] **T003** [P] [BLOCKS] Add `due_date` field to Task dataclass in src/models.py
  - Type: `datetime | None = None`
  - Optional field, defaults to None

- [ ] **T004** [P] [BLOCKS] Add timestamp fields to Task dataclass in src/models.py
  - `created_at: datetime = field(default_factory=datetime.now)`
  - `updated_at: datetime = field(default_factory=datetime.now)`
  - `completed_at: datetime | None = None`

- [ ] **T005** [P] Add `is_overdue()` method to Task dataclass in src/models.py
  - Returns True if due_date is past and task not completed
  - Returns False otherwise

- [ ] **T006** [P] Add `time_to_complete()` method to Task dataclass in src/models.py
  - Calculate duration from created_at to completed_at
  - Return formatted string: "2 hours 30 minutes"
  - Return None if not completed

- [ ] **T007** [P] Create Config dataclass in src/models.py
  - Fields: default_priority, list_view, auto_save, confirm_delete
  - Fields: data_file, config_file
  - All with sensible defaults

- [ ] **T008** [P] [BLOCKS] Create src/persistence.py module
  - Create DataStore class skeleton
  - Add __init__ method with data_file parameter

- [ ] **T009** [DEP: T008] Implement DataStore.load_tasks() in src/persistence.py
  - Read JSON file
  - Parse into Task objects
  - Handle missing file (return empty list)
  - Handle corrupted JSON (restore from backup)

- [ ] **T010** [DEP: T008] Implement DataStore.save_tasks() in src/persistence.py
  - Convert tasks to dict using asdict()
  - Write to JSON with indent=2
  - Use atomic write pattern (backup old, write new, delete backup)
  - Handle datetime serialization with default=str

- [ ] **T011** [DEP: T008] Implement DataStore.load_config() in src/persistence.py
  - Read config JSON file
  - Parse into Config object
  - Return default Config if file missing

- [ ] **T012** [DEP: T008] Implement DataStore.save_config() in src/persistence.py
  - Convert config to dict
  - Write to JSON file
  - Use atomic write pattern

---

## Phase 2: Enhanced Validators (1 hour)

### **T013-T020: Validation Functions**

- [ ] **T013** [P] [BLOCKS] Add `validate_priority()` function in src/validators.py
  - Input: priority string
  - Returns: error message or None
  - Valid: High, Medium, Low (case-insensitive)
  - Normalize to title case

- [ ] **T014** [P] [BLOCKS] Add `validate_tags()` function in src/validators.py
  - Input: list of tag strings
  - Returns: error message or None
  - Rules: max 10 tags, each 1-20 chars, alphanumeric + -_
  - Check each tag individually

- [ ] **T015** [P] [BLOCKS] Add `parse_due_date()` function in src/validators.py
  - Input: date string
  - Returns: datetime object or None
  - Support formats:
    - ISO: 2026-01-15
    - Relative: tomorrow, next week, in 3 days
    - Short: 01/15

- [ ] **T016** [P] Add `validate_search_keyword()` function in src/validators.py
  - Input: search keyword string
  - Returns: error message or None
  - Rule: minimum 2 characters

- [ ] **T017** [P] Add `format_due_date()` helper function in src/validators.py
  - Input: datetime or None, is_overdue bool
  - Returns: formatted string
  - Examples: "Jan 15", "Tomorrow", "⚠️ 2 days overdue"

- [ ] **T018** [P] Add `format_relative_time()` helper in src/validators.py
  - Input: datetime
  - Returns: relative time string
  - Examples: "2 hours ago", "Yesterday", "Just now"

- [ ] **T019** [P] Add `format_duration()` helper in src/validators.py
  - Input: timedelta
  - Returns: human-readable duration
  - Examples: "2h 30m", "3 days", "45 seconds"

- [ ] **T020** [P] Add `normalize_priority()` helper in src/validators.py
  - Input: priority string (any case)
  - Returns: title case priority or default "Medium"

---

## Phase 3: Filter & Search (2 hours)

### **T021-T030: Filter and Sort Logic**

- [ ] **T021** [P] [BLOCKS] Create src/filters.py module
  - Module docstring
  - Import statements

- [ ] **T022** [DEP: T021] [P] Implement `filter_by_status()` in src/filters.py
  - Input: tasks list, status string ("complete"/"incomplete"/"all")
  - Returns: filtered task list
  - Test with empty list

- [ ] **T023** [DEP: T021] [P] Implement `filter_by_priority()` in src/filters.py
  - Input: tasks list, priority string
  - Returns: filtered task list
  - Case-insensitive matching

- [ ] **T024** [DEP: T021] [P] Implement `filter_by_tag()` in src/filters.py
  - Input: tasks list, tag string
  - Returns: tasks containing that tag
  - Case-insensitive matching

- [ ] **T025** [DEP: T021] [P] Implement `filter_by_tags_any()` in src/filters.py
  - Input: tasks list, list of tags
  - Returns: tasks containing ANY of the tags (OR logic)
  - More flexible than single tag filter

- [ ] **T026** [DEP: T021] [P] Implement `search_tasks()` in src/filters.py
  - Input: tasks list, keyword string
  - Returns: tasks with keyword in title OR description
  - Case-insensitive matching

- [ ] **T027** [DEP: T021] [P] Implement `sort_tasks()` in src/filters.py
  - Input: tasks list, sort_by string, reverse bool
  - Returns: sorted task list
  - Support sort_by: id, title, priority, created, due

- [ ] **T028** [DEP: T027] [P] Add `_priority_sort_key()` helper in src/filters.py
  - Convert priority to sort order (High=0, Medium=1, Low=2)
  - Handle missing priority gracefully

- [ ] **T029** [DEP: T021] [P] Implement `combine_filters()` in src/filters.py
  - Input: tasks list, multiple filter criteria
  - Apply filters sequentially
  - Returns final filtered result

- [ ] **T030** [DEP: T021] [P] Add `highlight_matches()` helper in src/filters.py
  - Input: text, keyword
  - Returns: Rich Text object with highlighted matches
  - Use [yellow] tags for highlights

---

## Phase 4: Command Parser (2 hours)

### **T031-T039: Argument Parsing**

- [ ] **T031** [P] [BLOCKS] Create src/parsers.py module
  - Import argparse, typing
  - Create CommandParser class

- [ ] **T032** [DEP: T031] [P] Implement `parse_add_args()` in src/parsers.py
  - Use argparse.ArgumentParser
  - Flags: -t/--title, -d/--description, -p/--priority, --tags, --due
  - Handle SystemExit gracefully (return None on error)
  - Parse comma-separated tags

- [ ] **T033** [DEP: T031] [P] Implement `parse_list_args()` in src/parsers.py
  - Flags: -s/--status, -p/--priority, --tag, --sort, --reverse
  - Flags: --compact, --detailed
  - Return dict of parsed arguments

- [ ] **T034** [DEP: T031] [P] Implement `parse_update_args()` in src/parsers.py
  - First arg: task ID (required)
  - Flags: -t/--title, -d/--description, -p/--priority, --tags, --due
  - All flags optional (partial update support)

- [ ] **T035** [DEP: T031] [P] Implement `parse_complete_args()` in src/parsers.py
  - Accept multiple task IDs: /complete 1 2 3
  - Flag: --tag (complete by tag)
  - Flag: --all (complete all)

- [ ] **T036** [DEP: T031] [P] Implement `parse_delete_args()` in src/parsers.py
  - Accept multiple task IDs
  - Flag: --completed (delete all completed)
  - Flag: --force (skip confirmation)

- [ ] **T037** [DEP: T031] Implement `split_command_args()` helper in src/parsers.py
  - Input: full command string
  - Returns: (command, args_list)
  - Handle quoted strings properly

- [ ] **T038** [DEP: T031] Add `show_parser_error()` helper in src/parsers.py
  - Input: error message
  - Display helpful Rich panel with examples
  - Show correct usage

- [ ] **T039** [DEP: T031] Add unit tests for all parsers
  - Test valid inputs
  - Test invalid inputs
  - Test edge cases (empty, special chars)

---

## Phase 5: Enhanced Operations (2 hours)

### **T040-T052: TaskManager Extensions**

- [ ] **T040** [DEP: T008] Update TaskManager.__init__() in src/operations.py
  - Accept DataStore instance
  - Load tasks on initialization
  - Initialize next_id based on loaded tasks

- [ ] **T041** [DEP: T001, T002, T003, T004] Update TaskManager.add() in src/operations.py
  - Add parameters: priority, tags, due_date
  - Set created_at timestamp
  - Call _auto_save() after add

- [ ] **T042** [DEP: T001, T002, T003, T004] Update TaskManager.update() in src/operations.py
  - Support partial updates (all params optional except task_id)
  - Update updated_at timestamp
  - Call _auto_save() after update

- [ ] **T043** [DEP: T004] Update TaskManager.toggle_complete() in src/operations.py
  - Set completed_at timestamp when marking complete
  - Clear completed_at when marking incomplete
  - Update updated_at timestamp

- [ ] **T044** [P] Add TaskManager.complete_multiple() in src/operations.py
  - Input: list of task IDs
  - Mark each as complete
  - Return count of successfully completed

- [ ] **T045** [P] Add TaskManager.complete_all() in src/operations.py
  - Mark all incomplete tasks as complete
  - Set completed_at timestamps
  - Return count of tasks completed

- [ ] **T046** [P] Add TaskManager.complete_by_tag() in src/operations.py
  - Input: tag string
  - Complete all tasks with that tag
  - Return count

- [ ] **T047** [P] Add TaskManager.delete_multiple() in src/operations.py
  - Input: list of task IDs
  - Delete each task
  - Return count of deleted tasks

- [ ] **T048** [P] Add TaskManager.delete_completed() in src/operations.py
  - Remove all completed tasks
  - Return count of deleted tasks

- [ ] **T049** [P] Add TaskManager.get_statistics() in src/operations.py
  - Calculate total, completed, incomplete
  - Calculate completion rate percentage
  - Count by priority (High/Medium/Low)
  - Count top tags
  - Count overdue tasks
  - Return dict with all stats

- [ ] **T050** [P] Add TaskManager._auto_save() in src/operations.py
  - Check if auto_save enabled in config
  - Call data_store.save_tasks()
  - Handle save errors gracefully

- [ ] **T051** [P] Add TaskManager.export_json() in src/operations.py
  - Input: file path
  - Export all tasks to JSON
  - Return success message

- [ ] **T052** [P] Add TaskManager.import_json() in src/operations.py
  - Input: file path
  - Load tasks from JSON
  - Skip duplicates (check by title + created_at)
  - Return (imported_count, skipped_count)

---

## Phase 6: Rich Formatters (1.5 hours)

### **T053-T062: Formatting Utilities**

- [ ] **T053** [P] [BLOCKS] Create src/formatters.py module
  - Import Rich components
  - Module docstring

- [ ] **T054** [DEP: T053] [P] Implement `create_task_table()` in src/formatters.py
  - Input: tasks list, view_mode string
  - Returns: Rich Table object
  - Support modes: default, compact, detailed
  - Use appropriate box styles and colors

- [ ] **T055** [DEP: T053] [P] Implement `create_stats_panel()` in src/formatters.py
  - Input: stats dict
  - Returns: Rich Panel with formatted statistics
  - Use progress bars for completion rate
  - Color-code priority breakdown

- [ ] **T056** [DEP: T053] [P] Implement `create_task_detail_panel()` in src/formatters.py
  - Input: Task object
  - Returns: Rich Panel with full task details
  - Show all metadata fields
  - Highlight overdue status

- [ ] **T057** [DEP: T053] [P] Add `format_priority()` helper in src/formatters.py
  - Input: priority string
  - Returns: Rich formatted string with emoji and color
  - 🔴 High (red), 🟡 Medium (yellow), 🟢 Low (green)

- [ ] **T058** [DEP: T053] [P] Add `format_tags()` helper in src/formatters.py
  - Input: tags list
  - Returns: Rich formatted string
  - Format: [tag1] [tag2] [tag3]
  - Use magenta color

- [ ] **T059** [DEP: T053] [P] Add `create_confirmation_panel()` in src/formatters.py
  - Input: title, message, border_style
  - Returns: Rich Panel for confirmations
  - Used for success/error messages

- [ ] **T060** [DEP: T053] [P] Add `create_help_table()` in src/formatters.py
  - Create beautiful command reference table
  - Include aliases
  - Use DOUBLE box style

- [ ] **T061** [DEP: T053] [P] Add `create_search_results_table()` in src/formatters.py
  - Like create_task_table but with highlighted matches
  - Show search keyword in title
  - Display result count

- [ ] **T062** [DEP: T053] [P] Add `create_export_progress()` in src/formatters.py
  - Use Rich Progress bar
  - Show "Exporting tasks..." with spinner
  - Return context manager for with statement

---

## Phase 7: Enhanced CLI Commands (3 hours)

### **T063-T075: Command Implementation**

- [ ] **T063** [DEP: T032, T041] Update handle_add() in src/main.py
  - Parse command-line flags first
  - Fall back to interactive prompts if no flags
  - Validate all inputs
  - Use create_confirmation_panel() for success
  - Show full task details in panel

- [ ] **T064** [DEP: T033] Update handle_list() in src/main.py
  - Parse list flags (status, priority, tag, sort, view mode)
  - Apply filters using filters module
  - Apply sorting
  - Use create_task_table() with appropriate view mode
  - Show filter summary if filters applied

- [ ] **T065** [DEP: T034, T042] Update handle_update() in src/main.py
  - Parse update flags
  - Fall back to interactive prompts if no flags
  - Support partial updates
  - Show before/after in panel

- [ ] **T066** [DEP: T035, T044, T045, T046] Update handle_complete() in src/main.py
  - Support multiple IDs: /complete 1 2 3
  - Support /complete --all
  - Support /complete --tag <tag>
  - Show count: "✅ Marked X tasks as complete"

- [ ] **T067** [DEP: T036, T047, T048] Update handle_delete() in src/main.py
  - Support multiple IDs: /delete 1 2 3
  - Support /delete --completed
  - Always confirm unless --force flag
  - Show preview before deletion
  - Show count after deletion

- [ ] **T068** [DEP: T026] Add handle_search() in src/main.py
  - Parse /search <keyword>
  - Validate keyword length
  - Use search_tasks() from filters module
  - Display results with create_search_results_table()
  - Show count: "Found X tasks matching 'keyword'"

- [ ] **T069** [DEP: T056] Add handle_show() in src/main.py
  - Parse /show <id>
  - Validate task ID
  - Use create_task_detail_panel()
  - Show all task metadata

- [ ] **T070** [DEP: T049, T055] Add handle_stats() in src/main.py
  - Get statistics from TaskManager
  - Use create_stats_panel()
  - Display beautiful dashboard

- [ ] **T071** [DEP: T051] Add handle_export() in src/main.py
  - Parse /export <format> (json/csv/md)
  - Generate filename with timestamp
  - Call appropriate export function
  - Show success with file path

- [ ] **T072** [DEP: T052] Add handle_import() in src/main.py
  - Parse /import <file>
  - Validate file exists
  - Call TaskManager.import_json()
  - Show summary: "Imported X, skipped Y duplicates"

- [ ] **T073** Add handle_config() in src/main.py
  - /config - Show all settings in panel
  - /config set <key> <value> - Update setting
  - Save config to file
  - Show current value after update

- [ ] **T074** Add command aliases to main_loop() in src/main.py
  - Map /a → /add, /l → /list, /u → /update
  - Map /d → /delete, /c → /complete, /s → /search
  - Map /h → /help
  - Document aliases in help

- [ ] **T075** [DEP: T060] Update handle_help() in src/main.py
  - Use create_help_table()
  - Include all new commands
  - Show command aliases
  - Add usage examples

---

## Phase 8: Testing & Polish (1.5 hours)

### **T076-T078: Final Testing and Documentation**

- [ ] **T076** Manual testing checklist
  - Test all commands with valid inputs
  - Test all commands with invalid inputs
  - Test with empty task list
  - Test with 100+ tasks (performance)
  - Test JSON persistence (save/load)
  - Test file corruption recovery
  - Test all filter combinations
  - Test search with various keywords
  - Test bulk operations
  - Test export formats (JSON, CSV, MD)
  - Test import with duplicates
  - Test statistics accuracy
  - Test config management

- [ ] **T077** Update README.md with new features
  - Document all new commands
  - Add flag examples
  - Document new fields (priority, tags, due_date)
  - Add demo script
  - Update usage examples

- [ ] **T078** Create demo data setup script
  - Create demo_setup.py in scripts/
  - Generate realistic sample tasks
  - Mix of priorities, tags, statuses
  - Include overdue and completed tasks
  - Add comments explaining each task

---

## Dependency Graph

```
Phase 1 (Data Model):
T001-T004 [BLOCKS] → T041, T042, T043, T054
T008 [BLOCKS] → T009, T010, T011, T012, T040

Phase 2 (Validators):
T013, T014, T015 [BLOCKS] → T063, T064, T065

Phase 3 (Filters):
T021 [BLOCKS] → T022-T030
T022-T030 → T064, T068

Phase 4 (Parsers):
T031 [BLOCKS] → T032-T038
T032-T036 → T063-T067

Phase 5 (Operations):
T040-T052 → T063-T072

Phase 6 (Formatters):
T053 [BLOCKS] → T054-T062
T054-T062 → T064, T068, T069, T070, T075

Phase 7 (CLI):
Sequential implementation: T063 → T064 → ... → T075

Phase 8 (Testing):
T076 depends on ALL previous tasks
```

---

## Parallelization Strategy

### **Parallel Batch 1** (Phase 1 - Start together)
- T001, T002, T003, T004, T005, T006, T007, T008

### **Parallel Batch 2** (Phase 2 - Start together)
- T013, T014, T015, T016, T017, T018, T019, T020

### **Parallel Batch 3** (Phase 3 - After T021)
- T022, T023, T024, T025, T026, T027, T028, T029, T030

### **Parallel Batch 4** (Phase 4 - After T031)
- T032, T033, T034, T035, T036, T038

### **Parallel Batch 5** (Phase 5 - Mixed)
- T044, T045, T046, T047, T048, T049, T050, T051, T052

### **Parallel Batch 6** (Phase 6 - After T053)
- T054, T055, T056, T057, T058, T059, T060, T061, T062

### **Sequential** (Phase 7)
- T063 → T064 → T065 → T066 → T067 → T068 → T069 → T070 → T071 → T072 → T073 → T074 → T075

---

## Time Estimates

### **Optimistic** (experienced developer, no blockers)
- Phase 1: 2 hours
- Phase 2: 45 minutes
- Phase 3: 1.5 hours
- Phase 4: 1.5 hours
- Phase 5: 1.5 hours
- Phase 6: 1 hour
- Phase 7: 2.5 hours
- Phase 8: 1 hour
**Total: 12 hours**

### **Realistic** (normal development pace)
- Phase 1: 3 hours
- Phase 2: 1 hour
- Phase 3: 2 hours
- Phase 4: 2 hours
- Phase 5: 2 hours
- Phase 6: 1.5 hours
- Phase 7: 3 hours
- Phase 8: 1.5 hours
**Total: 16 hours**

### **Pessimistic** (learning, debugging, refactoring)
- Phase 1: 4 hours
- Phase 2: 1.5 hours
- Phase 3: 3 hours
- Phase 4: 3 hours
- Phase 5: 3 hours
- Phase 6: 2 hours
- Phase 7: 4 hours
- Phase 8: 2 hours
**Total: 22.5 hours**

---

## Critical Path

The critical path (longest dependency chain):
```
T008 → T010 → T040 → T041 → T063 → T076
```

**Estimated Critical Path Duration:** 6-8 hours

---

## Risk Mitigation Tasks

### **High Priority**
- T010: Atomic writes and backup handling
- T009: JSON corruption recovery
- T040: Safe task loading with migration

### **Medium Priority**
- T015: Date parsing edge cases
- T027: Sort performance with large datasets
- T063-T067: Command parsing error handling

---

## Testing Requirements

### **Unit Tests Needed**
- All validators (T013-T020)
- All filters (T022-T030)
- All parsers (T032-T036)
- Persistence (T009-T012)

### **Integration Tests Needed**
- End-to-end command flows
- JSON save/load cycle
- Filter + sort combinations
- Bulk operations

### **Manual Tests**
- Performance with 100+ tasks
- File corruption scenarios
- Demo script execution

---

## Acceptance Criteria (Per Phase)

### **Phase 1 Complete When:**
- ✅ Task model has all new fields
- ✅ JSON save/load works with new fields
- ✅ Auto-save triggers on operations
- ✅ File corruption recovery works

### **Phase 2 Complete When:**
- ✅ All new validators implemented
- ✅ Priority validation works
- ✅ Tag validation works
- ✅ Date parsing works for common formats

### **Phase 3 Complete When:**
- ✅ Filter by status works
- ✅ Filter by priority works
- ✅ Filter by tag works
- ✅ Search by keyword works
- ✅ Sort by all fields works

### **Phase 4 Complete When:**
- ✅ All command parsers implemented
- ✅ Flag parsing works for add/list/update
- ✅ Error handling works gracefully

### **Phase 5 Complete When:**
- ✅ TaskManager.add() accepts all new params
- ✅ TaskManager.update() supports partial updates
- ✅ Bulk operations (complete-all, delete-completed) work
- ✅ Statistics calculation accurate

### **Phase 6 Complete When:**
- ✅ All formatters implemented
- ✅ Tables render beautifully
- ✅ Panels look professional
- ✅ Colors and emojis consistent

### **Phase 7 Complete When:**
- ✅ All enhanced commands work
- ✅ All new commands work
- ✅ Command aliases work
- ✅ Help documentation complete

### **Phase 8 Complete When:**
- ✅ All manual tests pass
- ✅ No crashes on invalid input
- ✅ Performance acceptable
- ✅ Demo script runs flawlessly

---

## Next Steps

1. ✅ Spec approved
2. ✅ Plan approved
3. ✅ Tasks generated
4. ⏳ Begin Phase 1 implementation (T001-T012)
5. ⏳ Incremental testing after each phase
6. ⏳ Final demo preparation

---

**Status:** Ready for Implementation
**Last Updated:** 2026-01-05
**Estimated Start:** Immediate
**Estimated Completion:** 12-16 hours from start
