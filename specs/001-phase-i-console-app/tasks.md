# Tasks: Phase I - Todo In-Memory Python Console App

**Input**: Design documents from `/specs/001-phase-i-console-app/`
**Prerequisites**: plan.md (✅ complete), spec.md (✅ complete with 4 user stories)

**Tests**: Not requested - manual CLI testing only per plan.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/` at repository root (no tests/ directory for Phase I)
- Project structure: src/models.py, src/operations.py, src/validators.py, src/main.py

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Initialize UV project with pyproject.toml in repository root
- [ ] T002 Create src/ directory structure with __init__.py
- [ ] T003 Create README.md with setup instructions in repository root
- [ ] T004 Create CLAUDE.md with agent instructions in repository root

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 [P] Implement Task dataclass in src/models.py
- [ ] T006 [P] Implement sanitize_input() function in src/validators.py
- [ ] T007 [P] Implement validate_title() function in src/validators.py
- [ ] T008 [P] Implement validate_description() function in src/validators.py
- [ ] T009 [P] Implement validate_task_id() function in src/validators.py
- [ ] T010 [P] Implement TaskManager class initialization in src/operations.py
- [ ] T011 [P] Implement TaskManager.add() method in src/operations.py
- [ ] T012 [P] Implement TaskManager.get_all() method in src/operations.py
- [ ] T013 [P] Implement TaskManager.get_by_id() method in src/operations.py
- [ ] T014 Create main_loop() function skeleton in src/main.py
- [ ] T015 Implement command parsing logic in main_loop() function in src/main.py
- [ ] T016 [P] Implement handle_help() function in src/main.py
- [ ] T017 [P] Implement handle_exit() function in src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add tasks and view their todo list

**Independent Test**: Add multiple tasks with varying titles/descriptions, then view the complete list. Verify empty list shows friendly message.

### Implementation for User Story 1

- [ ] T018 [US1] Implement handle_add() function with title prompt in src/main.py
- [ ] T019 [US1] Add description prompt to handle_add() function in src/main.py
- [ ] T020 [US1] Add input validation and error handling to handle_add() in src/main.py
- [ ] T021 [US1] Add success confirmation message to handle_add() in src/main.py
- [ ] T022 [US1] Implement handle_list() function with empty list check in src/main.py
- [ ] T023 [US1] Add table header formatting to handle_list() in src/main.py
- [ ] T024 [US1] Add task iteration and display logic to handle_list() in src/main.py
- [ ] T025 [US1] Add status indicator (✓/✗) formatting to handle_list() in src/main.py
- [ ] T026 [US1] Add title/description truncation (50 chars) to handle_list() in src/main.py
- [ ] T027 [US1] Wire /add command to handle_add() in main_loop() in src/main.py
- [ ] T028 [US1] Wire /list command to handle_list() in main_loop() in src/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional - can add and view tasks

**Manual Testing**:
- [ ] Test: Add task with title only
- [ ] Test: Add task with title + description
- [ ] Test: Reject empty title
- [ ] Test: Reject title >200 characters
- [ ] Test: Reject description >1000 characters
- [ ] Test: Trim whitespace from title
- [ ] Test: View empty task list shows "No tasks yet. Add one with /add"
- [ ] Test: View task list with multiple tasks shows all tasks
- [ ] Test: Task IDs auto-increment (1, 2, 3...)

---

## Phase 4: User Story 2 - Mark Task Completion (Priority: P2)

**Goal**: Enable users to toggle task completion status

**Independent Test**: Create tasks, mark some complete, view list to verify status, toggle back to incomplete.

### Implementation for User Story 2

- [ ] T029 [P] [US2] Implement TaskManager.toggle_complete() method in src/operations.py
- [ ] T030 [US2] Implement handle_complete() function with ID prompt in src/main.py
- [ ] T031 [US2] Add ID validation to handle_complete() in src/main.py
- [ ] T032 [US2] Add error handling for non-existent task ID in handle_complete() in src/main.py
- [ ] T033 [US2] Add status confirmation message to handle_complete() in src/main.py
- [ ] T034 [US2] Wire /complete command to handle_complete() in main_loop() in src/main.py

**Checkpoint**: At this point, User Story 2 should be fully functional - can toggle task completion

**Manual Testing**:
- [ ] Test: Mark incomplete task as complete (status changes to ✓)
- [ ] Test: Mark complete task as incomplete (status toggles to ✗)
- [ ] Test: Error "Task #99 not found" for invalid ID
- [ ] Test: View list shows correct status indicators

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Enable users to update task titles and descriptions

**Independent Test**: Create task, update just title, update just description, update both simultaneously.

### Implementation for User Story 3

- [ ] T035 [P] [US3] Implement TaskManager.update() method in src/operations.py
- [ ] T036 [US3] Implement handle_update() function with ID prompt in src/main.py
- [ ] T037 [US3] Add ID validation to handle_update() in src/main.py
- [ ] T038 [US3] Add "Update title? (y/n)" prompt to handle_update() in src/main.py
- [ ] T039 [US3] Add new title prompt and validation to handle_update() in src/main.py
- [ ] T040 [US3] Add "Update description? (y/n)" prompt to handle_update() in src/main.py
- [ ] T041 [US3] Add new description prompt and validation to handle_update() in src/main.py
- [ ] T042 [US3] Add check for "no fields selected" to handle_update() in src/main.py
- [ ] T043 [US3] Add success confirmation message to handle_update() in src/main.py
- [ ] T044 [US3] Wire /update command to handle_update() in main_loop() in src/main.py

**Checkpoint**: At this point, User Story 3 should be fully functional - can update tasks

**Manual Testing**:
- [ ] Test: Update only title (description unchanged)
- [ ] Test: Update only description (title unchanged)
- [ ] Test: Update both title and description
- [ ] Test: Error "Task #99 not found" for invalid ID
- [ ] Test: Error when no fields selected for update
- [ ] Test: Validation errors for invalid title/description

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Enable users to delete tasks they no longer need

**Independent Test**: Create tasks, delete specific ones, verify they no longer appear in list.

### Implementation for User Story 4

- [ ] T045 [P] [US4] Implement TaskManager.delete() method in src/operations.py
- [ ] T046 [US4] Implement handle_delete() function with ID prompt in src/main.py
- [ ] T047 [US4] Add ID validation to handle_delete() in src/main.py
- [ ] T048 [US4] Add task details display before confirmation in handle_delete() in src/main.py
- [ ] T049 [US4] Add "Confirm (y/n)" prompt to handle_delete() in src/main.py
- [ ] T050 [US4] Add confirmation check and cancellation message to handle_delete() in src/main.py
- [ ] T051 [US4] Add task deletion and success message to handle_delete() in src/main.py
- [ ] T052 [US4] Wire /delete command to handle_delete() in main_loop() in src/main.py

**Checkpoint**: All user stories should now be independently functional

**Manual Testing**:
- [ ] Test: Delete existing task after confirmation
- [ ] Test: Error "Task #99 not found" for invalid ID
- [ ] Test: Cancel deletion (task remains in list)
- [ ] Test: Verify deleted task no longer appears in /list

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Refinements that affect multiple user stories

- [ ] T053 [P] Add input retry loops for validation failures across all command handlers in src/main.py
- [ ] T054 [P] Add error message for invalid commands in main_loop() in src/main.py
- [ ] T055 [P] Add welcome message at application start in src/main.py
- [ ] T056 [P] Add goodbye message to handle_exit() in src/main.py
- [ ] T057 [P] Add docstrings to all public functions in src/models.py
- [ ] T058 [P] Add docstrings to all public functions in src/validators.py
- [ ] T059 [P] Add docstrings to all public functions in src/operations.py
- [ ] T060 [P] Add docstrings to all public functions in src/main.py
- [ ] T061 [P] Add type hints verification across all modules
- [ ] T062 [P] Add constants for MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH in src/validators.py
- [ ] T063 Update README.md with complete usage examples and edge cases
- [ ] T064 Final manual testing of complete application workflow

**Checkpoint**: Application polished and ready for demo

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (US1 → US2 → US3 → US4)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independent)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independent)
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independent)

**Key Insight**: All 4 user stories are independent and can be implemented in parallel by different developers after Phase 2 completes.

### Within Each User Story

- Tasks within a story should be executed in order (T018 → T019 → ... → T028 for US1)
- Tasks marked [P] at the same level can run in parallel (e.g., T018-T021 could be done by one dev, T022-T026 by another)

### Parallel Opportunities

- **Phase 1 (Setup)**: All tasks marked [P] can run in parallel (T001-T004 can be done simultaneously)
- **Phase 2 (Foundational)**: Tasks T005-T013 can run in parallel (different files, no dependencies)
- **Phase 3-6 (User Stories)**: ALL user stories can be developed in parallel after Phase 2:
  - Developer A: User Story 1 (T018-T028)
  - Developer B: User Story 2 (T029-T034)
  - Developer C: User Story 3 (T035-T044)
  - Developer D: User Story 4 (T045-T052)
- **Phase 7 (Polish)**: Tasks T053-T062 can run in parallel (documentation and docstrings)

---

## Parallel Example: User Story 1

```bash
# After Foundational phase completes, launch User Story 1 tasks:

# Developer A (UI prompts):
Task T018: Implement handle_add() with title prompt
Task T019: Add description prompt
Task T020: Add validation
Task T021: Add success message

# Developer B (display logic) - can work in parallel:
Task T022: Implement handle_list() with empty check
Task T023: Add table header
Task T024: Add task iteration
Task T025: Add status indicators
Task T026: Add truncation

# Developer C (integration) - depends on A and B:
Task T027: Wire /add to main_loop
Task T028: Wire /list to main_loop
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T017) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 (T018-T028)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Demo basic todo app with add/list functionality

**MVP Deliverable**: Working CLI todo app that can add and view tasks

### Incremental Delivery (Recommended)

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → **MVP!** (can demo)
3. Add User Story 2 → Test independently → **V1.1** (completion tracking)
4. Add User Story 3 → Test independently → **V1.2** (task editing)
5. Add User Story 4 → Test independently → **V1.3** (task deletion)
6. Add Polish → **V1.4** (production ready)

Each increment adds value without breaking previous functionality.

### Parallel Team Strategy

With 4 developers after Foundational phase:

1. Team completes Setup + Foundational together (T001-T017)
2. Once Foundational is done (checkpoint reached):
   - **Dev A**: User Story 1 - Create and View Tasks (T018-T028)
   - **Dev B**: User Story 2 - Mark Completion (T029-T034)
   - **Dev C**: User Story 3 - Update Tasks (T035-T044)
   - **Dev D**: User Story 4 - Delete Tasks (T045-T052)
3. Stories complete independently, integrate via main_loop
4. Team converges for Polish phase (T053-T064)

---

## Task Count Summary

| Phase | Task Count | Parallelizable | Notes |
|-------|-----------|----------------|-------|
| Phase 1: Setup | 4 | 4 (100%) | Project initialization |
| Phase 2: Foundational | 13 | 12 (92%) | Core infrastructure |
| Phase 3: User Story 1 (P1) | 11 | 4 (36%) | Add/view tasks - MVP |
| Phase 4: User Story 2 (P2) | 6 | 1 (17%) | Toggle completion |
| Phase 5: User Story 3 (P3) | 10 | 1 (10%) | Update task details |
| Phase 6: User Story 4 (P4) | 8 | 1 (13%) | Delete tasks |
| Phase 7: Polish | 12 | 11 (92%) | Documentation and refinement |
| **Total** | **64** | **34 (53%)** | ~300-500 LOC |

---

## Notes

- **[P] tasks** = different files, no dependencies - safe to parallelize
- **[Story] labels** = map task to specific user story for traceability (US1, US2, US3, US4)
- **Each user story is independently completable** and testable
- **No automated tests** in Phase I - manual CLI testing only per plan
- **Stop at any checkpoint** to validate story independently before continuing
- **Commit frequently** - ideally after each task or logical group
- **All code generated by Claude Code** from these task specifications
- **File paths are explicit** in each task description for clarity
- **Task IDs reference** required in all commits per constitution

---

## Validation Checklist

Before marking Phase 7 complete, verify:

- [ ] All 64 tasks completed and checked off
- [ ] All 5 core features functional (/add, /list, /update, /delete, /complete)
- [ ] Manual testing checklist complete (see plan.md Testing Strategy)
- [ ] README.md has setup and usage instructions
- [ ] CLAUDE.md has agent instructions
- [ ] All functions have type hints
- [ ] All public functions have docstrings
- [ ] Error messages match specified format
- [ ] Whitespace trimming works correctly
- [ ] Task IDs auto-increment properly
- [ ] Empty list shows friendly message
- [ ] Can complete full task lifecycle in <60 seconds
- [ ] No crashes on invalid input
- [ ] /help shows all commands
- [ ] /exit terminates cleanly

---

**Generated**: 2025-12-31
**Total Tasks**: 64
**Parallel Opportunities**: 34 tasks (53%)
**MVP Scope**: Phases 1-3 (28 tasks, User Story 1 only)
**Full Scope**: All 7 phases (64 tasks, all 4 user stories)
**Estimated LOC**: 300-500 lines
