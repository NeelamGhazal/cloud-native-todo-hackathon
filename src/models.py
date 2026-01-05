"""Data models for the todo application.

This module defines the Task entity using Python dataclasses.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """Represents a todo task with metadata.

    Attributes:
        id: Unique integer identifier (auto-generated, sequential)
        title: Short description (1-200 characters, required)
        description: Detailed notes (0-1000 characters, optional)
        completed: Completion status (default: False)
        priority: Priority level (High, Medium, Low)
        tags: List of category tags
        created_at: Creation timestamp
        updated_at: Last update timestamp
        completed_at: Completion timestamp (None if not completed)
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    priority: str = "Medium"
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None

    def time_to_complete(self) -> str | None:
        """Calculate time taken to complete task.

        Returns:
            Human-readable duration string or None if not completed
        """
        if self.completed_at:
            delta = self.completed_at - self.created_at
            hours = delta.total_seconds() / 3600
            if hours < 1:
                minutes = int(delta.total_seconds() / 60)
                return f"{minutes}m"
            elif hours < 24:
                return f"{int(hours)}h {int((hours % 1) * 60)}m"
            else:
                days = int(hours / 24)
                return f"{days}d {int(hours % 24)}h"
        return None


@dataclass
class Config:
    """User configuration settings.

    Attributes:
        default_priority: Default priority for new tasks
        auto_save: Enable automatic JSON persistence
        data_file: Path to task data JSON file
        config_file: Path to config JSON file
    """
    default_priority: str = "Medium"
    auto_save: bool = True
    data_file: str = ".todo-data.json"
    config_file: str = ".todo-config.json"
