"""Task management operations for the todo application.

This module provides the TaskManager class for CRUD operations on tasks.
"""

from src.models import Task


class TaskManager:
    """Manages the in-memory task list with CRUD operations.

    Attributes:
        tasks: List of Task objects stored in memory
        next_id: Counter for auto-generating sequential task IDs
    """

    def __init__(self) -> None:
        """Initialize the TaskManager with an empty task list."""
        self.tasks: list[Task] = []
        self.next_id: int = 1

    def add(self, title: str, description: str = "") -> Task:
        """Add a new task to the list.

        Args:
            title: Task title (pre-validated)
            description: Task description (pre-validated, optional)

        Returns:
            The newly created Task object with auto-generated ID
        """
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            completed=False
        )
        self.tasks.append(task)
        self.next_id += 1
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

    def update(self, task_id: int, title: str | None = None, description: str | None = None) -> Task | None:
        """Update a task's title and/or description.

        Args:
            task_id: The unique task identifier
            title: New title (if provided)
            description: New description (if provided)

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
        return task
