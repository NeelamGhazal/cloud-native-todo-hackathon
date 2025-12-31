"""Input validation functions for the todo application.

This module provides validation for user inputs including title, description,
and task ID validation.
"""

# Validation constants
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000


def sanitize_input(text: str) -> str:
    """Trim leading and trailing whitespace from input text.

    Args:
        text: The input text to sanitize

    Returns:
        The sanitized text with leading/trailing whitespace removed
    """
    return text.strip()


def validate_title(title: str) -> str | None:
    """Validate a task title.

    Args:
        title: The title to validate (should be pre-sanitized)

    Returns:
        Error message if validation fails, None if valid

    Validation rules:
        - Must not be empty or whitespace-only (after trimming)
        - Must be 1-200 characters
    """
    if not title:
        return "Title cannot be empty"

    if len(title) > MAX_TITLE_LENGTH:
        return f"Title must be 1-{MAX_TITLE_LENGTH} characters"

    return None


def validate_description(description: str) -> str | None:
    """Validate a task description.

    Args:
        description: The description to validate (should be pre-sanitized)

    Returns:
        Error message if validation fails, None if valid

    Validation rules:
        - Optional (empty string is allowed)
        - Must be 0-1000 characters
    """
    if len(description) > MAX_DESCRIPTION_LENGTH:
        return f"Description must be 0-{MAX_DESCRIPTION_LENGTH} characters"

    return None


def validate_task_id(task_id_str: str) -> tuple[int | None, str | None]:
    """Validate and parse a task ID input.

    Args:
        task_id_str: The task ID string to validate

    Returns:
        Tuple of (parsed_id, error_message)
        - If valid: (int, None)
        - If invalid: (None, error_message)

    Validation rules:
        - Must be a positive integer
        - Must be parseable as an integer
    """
    try:
        task_id = int(task_id_str)
        if task_id <= 0:
            return None, "Task ID must be a positive integer"
        return task_id, None
    except ValueError:
        return None, "Task ID must be a valid integer"
