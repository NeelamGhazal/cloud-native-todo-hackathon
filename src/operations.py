"""Task management operations for the todo application.

This module provides the TaskManager class for CRUD operations on tasks.
"""

from datetime import datetime
from src.models import Task, Config
from src.persistence import DataStore


class TaskManager:
    """Manages the in-memory task list with CRUD operations and persistence.

    Attributes:
        tasks: List of Task objects stored in memory
        next_id: Counter for auto-generating sequential task IDs
        data_store: DataStore instance for JSON persistence
        config: User configuration settings
    """

    def __init__(self, data_store: DataStore | None = None) -> None:
        """Initialize the TaskManager and load existing tasks.

        Args:
            data_store: Optional DataStore instance. Creates default if None.
        """
        self.data_store = data_store or DataStore()
        self.config = self.data_store.load_config()
        self.tasks: list[Task] = self.data_store.load_tasks()
        self.next_id: int = self._calculate_next_id()

    def _calculate_next_id(self) -> int:
        """Calculate the next available task ID.

        Returns:
            Next ID to use (max existing ID + 1, or 1 if no tasks)
        """
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

    def add(
        self,
        title: str,
        description: str = "",
        priority: str = "Medium",
        tags: list[str] | None = None
    ) -> Task:
        """Add a new task to the list.

        Args:
            title: Task title (pre-validated)
            description: Task description (pre-validated, optional)
            priority: Priority level (High, Medium, Low)
            tags: List of category tags

        Returns:
            The newly created Task object with auto-generated ID
        """
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            completed=False,
            priority=priority,
            tags=tags or [],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.tasks.append(task)
        self.next_id += 1
        self._auto_save()
        return task

    def get_all(self) -> list[Task]:
        """Retrieve all tasks.

        Returns:
            List of all Task objects (may be empty)
        """
        return self.tasks

    def get_by_id(self, task_id: int) -> Task | None:
        """Retrieve a task by its ID.

        Args:
            task_id: The unique task identifier

        Returns:
            The Task object if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        priority: str | None = None,
        tags: list[str] | None = None
    ) -> Task | None:
        """Update a task's fields (supports partial updates).

        Args:
            task_id: The unique task identifier
            title: New title (if provided)
            description: New description (if provided)
            priority: New priority (if provided)
            tags: New tags list (if provided)

        Returns:
            The updated Task object if found, None otherwise
        """
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

        task.updated_at = datetime.now()
        self._auto_save()
        return task

    def delete(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Args:
            task_id: The unique task identifier

        Returns:
            True if task was deleted, False if task not found
        """
        task = self.get_by_id(task_id)
        if task is None:
            return False

        self.tasks.remove(task)
        self._auto_save()
        return True

    def toggle_complete(self, task_id: int) -> Task | None:
        """Toggle a task's completion status.

        Args:
            task_id: The unique task identifier

        Returns:
            The updated Task object if found, None otherwise
        """
        task = self.get_by_id(task_id)
        if task is None:
            return None

        task.completed = not task.completed
        task.completed_at = datetime.now() if task.completed else None
        task.updated_at = datetime.now()
        self._auto_save()
        return task

    def get_statistics(self) -> dict:
        """Calculate task statistics.

        Returns:
            Dictionary with stats:
                - total: Total task count
                - completed: Completed task count
                - incomplete: Incomplete task count
                - completion_rate: Percentage completed
                - by_priority: Count by priority level
        """
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t.completed])
        incomplete = total - completed

        # Priority breakdown
        high = len([t for t in self.tasks if t.priority == "High"])
        medium = len([t for t in self.tasks if t.priority == "Medium"])
        low = len([t for t in self.tasks if t.priority == "Low"])

        # Completion rate
        rate = (completed / total * 100) if total > 0 else 0

        return {
            "total": total,
            "completed": completed,
            "incomplete": incomplete,
            "completion_rate": rate,
            "by_priority": {"High": high, "Medium": medium, "Low": low}
        }

    def _auto_save(self) -> None:
        """Auto-save tasks to JSON if enabled in config."""
        if self.config.auto_save:
            try:
                self.data_store.save_tasks(self.tasks)
            except Exception:
                # Silent fail - don't disrupt user operations
                pass
