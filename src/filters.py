"""Filter and search operations for tasks.

This module provides filtering, sorting, and searching functionality for task lists.
"""

from typing import List, Callable
from datetime import datetime

from src.models import Task


def filter_by_status(tasks: List[Task], status: str) -> List[Task]:
    """Filter tasks by completion status.

    Args:
        tasks: List of tasks to filter
        status: Status filter ("complete", "incomplete", or "all")

    Returns:
        Filtered list of tasks
    """
    if status.lower() == "complete":
        return [t for t in tasks if t.completed]
    elif status.lower() == "incomplete":
        return [t for t in tasks if not t.completed]
    else:  # all
        return tasks


def filter_by_priority(tasks: List[Task], priority: str) -> List[Task]:
    """Filter tasks by priority level.

    Args:
        tasks: List of tasks to filter
        priority: Priority filter ("High", "Medium", or "Low")

    Returns:
        Filtered list of tasks
    """
    return [t for t in tasks if t.priority.lower() == priority.lower()]


def filter_by_tag(tasks: List[Task], tag: str) -> List[Task]:
    """Filter tasks containing the specified tag.

    Args:
        tasks: List of tasks to filter
        tag: Tag to search for (case-insensitive)

    Returns:
        Filtered list of tasks containing the tag
    """
    tag_lower = tag.lower()
    return [t for t in tasks if tag_lower in [t_tag.lower() for t_tag in t.tags]]


def search_tasks(tasks: List[Task], keyword: str) -> List[Task]:
    """Search tasks by keyword in title or description.

    Args:
        tasks: List of tasks to search
        keyword: Keyword to search for (case-insensitive)

    Returns:
        List of tasks containing the keyword
    """
    keyword_lower = keyword.lower()
    return [
        t for t in tasks
        if keyword_lower in t.title.lower() or keyword_lower in t.description.lower()
    ]


def sort_tasks(
    tasks: List[Task],
    sort_by: str = "id",
    reverse: bool = False
) -> List[Task]:
    """Sort tasks by specified field.

    Args:
        tasks: List of tasks to sort
        sort_by: Field to sort by ("id", "title", "priority", "created")
        reverse: Whether to reverse the sort order

    Returns:
        Sorted list of tasks
    """
    sort_keys: dict[str, Callable] = {
        "id": lambda t: t.id,
        "title": lambda t: t.title.lower(),
        "priority": lambda t: _priority_sort_key(t.priority),
        "created": lambda t: t.created_at,
    }

    key_func = sort_keys.get(sort_by.lower(), lambda t: t.id)
    return sorted(tasks, key=key_func, reverse=reverse)


def _priority_sort_key(priority: str) -> int:
    """Convert priority to sort key for sorting.

    Args:
        priority: Priority level

    Returns:
        Sort key (High=0, Medium=1, Low=2, Unknown=3)
    """
    priority_order = {"high": 0, "medium": 1, "low": 2}
    return priority_order.get(priority.lower(), 3)
