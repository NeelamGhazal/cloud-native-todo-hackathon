"""Main CLI interface for the todo application.

This module provides the command-line interface and entry point for the application.
"""

from src.operations import TaskManager
from src.validators import sanitize_input, validate_title, validate_description, validate_task_id


def main_loop() -> None:
    """Main command loop for the todo application.

    Handles command parsing and routing to appropriate handler functions.
    """
    # Initialize the task manager
    manager = TaskManager()

    # Print welcome message
    print("Welcome to Todo App! Type /help for available commands.")
    print()

    # Main loop
    while True:
        try:
            # Get user command
            command = input("> ").strip().lower()

            # Parse and route command
            if command == "/help":
                handle_help()
            elif command == "/exit":
                handle_exit()
                break
            elif command == "/add":
                handle_add(manager)
            elif command == "/list":
                handle_list(manager)
            elif command == "/complete":
                # TODO: Implement in T030
                print("Not yet implemented")
            elif command == "/update":
                # TODO: Implement in T036
                print("Not yet implemented")
            elif command == "/delete":
                # TODO: Implement in T046
                print("Not yet implemented")
            elif command == "":
                # Empty input - ignore
                continue
            else:
                print(f"Error: Unknown command '{command}'. Type /help for available commands.")
                print()

        except KeyboardInterrupt:
            print()
            print("Use /exit to quit")
            print()
        except EOFError:
            print()
            break


def handle_help() -> None:
    """Display available commands and their descriptions."""
    print("Available commands:")
    print("  /add       - Add a new task")
    print("  /list      - View all tasks")
    print("  /complete  - Toggle task completion status")
    print("  /update    - Update task title and/or description")
    print("  /delete    - Delete a task")
    print("  /help      - Show this help message")
    print("  /exit      - Exit the application")
    print()


def handle_list(manager: TaskManager) -> None:
    """Display all tasks in a formatted table.

    Args:
        manager: The TaskManager instance to retrieve tasks from
    """
    # Get all tasks
    tasks = manager.get_all()

    # Check if list is empty
    if not tasks:
        print("No tasks yet. Add one with /add")
        print()
        return

    # Print table header
    print("ID | Status | Title                    | Description")
    print("---+--------+--------------------------+----------------------------------")

    # Print each task
    for task in tasks:
        # Status indicator
        status = "✓" if task.completed else "✗"

        # Truncate title and description to 50 characters
        title_display = task.title[:50]
        if len(task.title) > 50:
            title_display = task.title[:47] + "..."

        description_display = task.description[:50]
        if len(task.description) > 50:
            description_display = task.description[:47] + "..."

        # Print formatted row
        print(f"{task.id:<2} | {status:<6} | {title_display:<24} | {description_display}")

    print()


def handle_add(manager: TaskManager) -> None:
    """Handle adding a new task with title and description prompts.

    Args:
        manager: The TaskManager instance to add the task to
    """
    # Prompt for title
    title_input = input("Enter task title: ")
    title = sanitize_input(title_input)

    # Validate title
    error = validate_title(title)
    if error:
        print(f"Error: {error}")
        print()
        return

    # Prompt for description (optional)
    description_input = input("Enter description (optional): ")
    description = sanitize_input(description_input)

    # Validate description
    error = validate_description(description)
    if error:
        print(f"Error: {error}")
        print()
        return

    # Add task
    task = manager.add(title, description)

    # Success confirmation
    print(f"✓ Task #{task.id} added successfully")
    print()


def handle_exit() -> None:
    """Handle application exit."""
    print("Goodbye!")


def main() -> None:
    """Entry point for the application."""
    main_loop()


if __name__ == "__main__":
    main()
