"""Data models for the todo application.

This module defines the Task entity using Python dataclasses.
"""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a todo task.

    Attributes:
        id: Unique integer identifier (auto-generated, sequential)
        title: Short description (1-200 characters, required)
        description: Detailed notes (0-1000 characters, optional)
        completed: Completion status (default: False)
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
