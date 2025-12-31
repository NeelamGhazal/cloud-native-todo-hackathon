"""Main CLI interface for the todo application.

This module provides the command-line interface and entry point for the application.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

from src.operations import TaskManager
from src.validators import sanitize_input, validate_title, validate_description, validate_task_id

# Initialize rich console
console = Console()


def show_banner() -> None:
    """Display the application banner with ASCII art."""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║          ████████╗ ██████╗ ██████╗  ██████╗                 ║
    ║          ╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗                ║
    ║             ██║   ██║   ██║██║  ██║██║   ██║                ║
    ║             ██║   ██║   ██║██║  ██║██║   ██║                ║
    ║             ██║   ╚██████╔╝██████╔╝╚██████╔╝                ║
    ║             ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝                 ║
    ║                                                              ║
    ║                    PHASE I - CONSOLE APP                    ║
    ║              Spec-Driven Development Demo                   ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")
    console.print(
        Panel.fit(
            "✨ [bold yellow]Welcome to Todo App![/bold yellow] ✨\n"
            "Type [bold cyan]/help[/bold cyan] for available commands",
            border_style="cyan",
            padding=(1, 2)
        )
    )
    console.print()


def main_loop() -> None:
    """Main command loop for the todo application.

    Handles command parsing and routing to appropriate handler functions.
    """
    # Initialize the task manager
    manager = TaskManager()

    # Show banner
    show_banner()

    # Main loop
    while True:
        try:
            # Get user command with colorful prompt
            console.print("📝", style="bold yellow", end=" ")
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
                handle_complete(manager)
            elif command == "/update":
                handle_update(manager)
            elif command == "/delete":
                handle_delete(manager)
            elif command == "":
                # Empty input - ignore
                continue
            else:
                console.print(
                    f"❌ [bold red]Error:[/bold red] Unknown command '{command}'.",
                    style="red"
                )
                console.print("Type [bold cyan]/help[/bold cyan] for available commands.\n")

        except KeyboardInterrupt:
            console.print()
            console.print("[yellow]💡 Use /exit to quit[/yellow]")
            console.print()
        except EOFError:
            console.print()
            break


def handle_help() -> None:
    """Display available commands in a beautiful table."""
    table = Table(
        title="📚 [bold cyan]Available Commands[/bold cyan]",
        box=box.DOUBLE,
        show_header=True,
        header_style="bold cyan",
        border_style="cyan"
    )

    table.add_column("Command", style="bold cyan", width=15)
    table.add_column("Description", style="white", width=45)

    table.add_row("/add", "Add a new task")
    table.add_row("/list", "View all tasks")
    table.add_row("/complete", "Toggle task completion status")
    table.add_row("/update", "Update task title and/or description")
    table.add_row("/delete", "Delete a task")
    table.add_row("/help", "Show this help message")
    table.add_row("/exit", "Exit the application")

    console.print(table)
    console.print()


def handle_list(manager: TaskManager) -> None:
    """Display all tasks in a formatted table.

    Args:
        manager: The TaskManager instance to retrieve tasks from
    """
    # Get all tasks
    tasks = manager.get_all()

    # Check if list is empty
    if not tasks:
        console.print(
            Panel.fit(
                "📭 [yellow]No tasks yet. Add one with[/yellow] [bold cyan]/add[/bold cyan]",
                border_style="yellow",
                padding=(1, 2)
            )
        )
        console.print()
        return

    # Create beautiful table
    table = Table(
        title="📋 [bold cyan]Your Tasks[/bold cyan]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold",
        border_style="cyan",
        expand=False
    )

    table.add_column("ID", style="bold cyan", justify="center", width=5)
    table.add_column("Status", justify="center", width=8)
    table.add_column("Title", style="yellow", width=30)
    table.add_column("Description", style="white", width=40)

    # Print each task
    for task in tasks:
        # Status indicator with color
        if task.completed:
            status = "[bold green]✅[/bold green]"
        else:
            status = "[bold red]❌[/bold red]"

        # Truncate title and description to fit columns
        title_display = task.title[:30]
        if len(task.title) > 30:
            title_display = task.title[:27] + "..."

        description_display = task.description[:40] if task.description else ""
        if len(task.description) > 40:
            description_display = task.description[:37] + "..."

        # Add row to table
        table.add_row(
            str(task.id),
            status,
            title_display,
            description_display
        )

    console.print(table)
    console.print()


def handle_delete(manager: TaskManager) -> None:
    """Handle deleting a task with confirmation.

    Args:
        manager: The TaskManager instance to delete task from
    """
    # Prompt for task ID
    console.print("[cyan]Enter task ID:[/cyan] ", end="")
    task_id_input = input()

    # Validate and parse task ID
    task_id, error = validate_task_id(task_id_input)
    if error:
        console.print(f"❌ [bold red]Error:[/bold red] {error}\n", style="red")
        return

    # Check if task exists and display details
    task = manager.get_by_id(task_id)
    if task is None:
        console.print(f"❌ [bold red]Error:[/bold red] Task #{task_id} not found\n", style="red")
        return

    # Display task details before confirmation in a warning panel
    task_info = f"[bold]Task #{task.id}:[/bold] {task.title}"
    if task.description:
        task_info += f"\n[dim]Description:[/dim] {task.description}"

    console.print(
        Panel.fit(
            task_info,
            title="⚠️  [bold yellow]Confirm Deletion[/bold yellow]",
            border_style="yellow",
            padding=(1, 2)
        )
    )

    # Confirm deletion
    console.print("[yellow]Confirm deletion (y/n):[/yellow] ", end="")
    confirm_input = input().strip().lower()

    # Check confirmation
    if confirm_input != "y":
        console.print("[yellow]Deletion cancelled[/yellow]\n")
        return

    # Delete task
    manager.delete(task_id)

    # Success message
    console.print(f"✅ [bold green]Task #{task_id} deleted successfully[/bold green]\n")


def handle_update(manager: TaskManager) -> None:
    """Handle updating task title and/or description.

    Args:
        manager: The TaskManager instance to update task in
    """
    # Prompt for task ID
    console.print("[cyan]Enter task ID:[/cyan] ", end="")
    task_id_input = input()

    # Validate and parse task ID
    task_id, error = validate_task_id(task_id_input)
    if error:
        console.print(f"❌ [bold red]Error:[/bold red] {error}\n", style="red")
        return

    # Check if task exists
    task = manager.get_by_id(task_id)
    if task is None:
        console.print(f"❌ [bold red]Error:[/bold red] Task #{task_id} not found\n", style="red")
        return

    # Ask if user wants to update title
    console.print("[cyan]Update title? (y/n):[/cyan] ", end="")
    update_title_input = input().strip().lower()
    new_title = None
    if update_title_input == "y":
        console.print("[cyan]Enter new title:[/cyan] ", end="")
        title_input = input()
        new_title = sanitize_input(title_input)

        # Validate title
        error = validate_title(new_title)
        if error:
            console.print(f"❌ [bold red]Error:[/bold red] {error}\n", style="red")
            return

    # Ask if user wants to update description
    console.print("[cyan]Update description? (y/n):[/cyan] ", end="")
    update_description_input = input().strip().lower()
    new_description = None
    if update_description_input == "y":
        console.print("[cyan]Enter new description:[/cyan] ", end="")
        description_input = input()
        new_description = sanitize_input(description_input)

        # Validate description
        error = validate_description(new_description)
        if error:
            console.print(f"❌ [bold red]Error:[/bold red] {error}\n", style="red")
            return

    # Check if at least one field is selected
    if new_title is None and new_description is None:
        console.print("❌ [bold red]Error:[/bold red] No fields selected for update\n", style="red")
        return

    # Update task
    updated_task = manager.update(task_id, title=new_title, description=new_description)

    # Success confirmation with task details
    task_info = f"[bold]Task #{updated_task.id}[/bold]\n"
    task_info += f"Title: {updated_task.title}\n"
    task_info += f"Description: {updated_task.description}"

    console.print(
        Panel.fit(
            task_info,
            title="✅ [bold green]Task Updated Successfully[/bold green]",
            border_style="green",
            padding=(1, 2)
        )
    )
    console.print()


def handle_complete(manager: TaskManager) -> None:
    """Handle toggling task completion status.

    Args:
        manager: The TaskManager instance to toggle task in
    """
    # Prompt for task ID
    console.print("[cyan]Enter task ID:[/cyan] ", end="")
    task_id_input = input()

    # Validate and parse task ID
    task_id, error = validate_task_id(task_id_input)
    if error:
        console.print(f"❌ [bold red]Error:[/bold red] {error}\n", style="red")
        return

    # Toggle completion status
    task = manager.toggle_complete(task_id)

    # Check if task exists
    if task is None:
        console.print(f"❌ [bold red]Error:[/bold red] Task #{task_id} not found\n", style="red")
        return

    # Confirmation message with status
    status = "complete ✅" if task.completed else "incomplete ❌"
    console.print(f"✅ [bold green]Task #{task.id} marked as {status}[/bold green]\n")


def handle_add(manager: TaskManager) -> None:
    """Handle adding a new task with title and description prompts.

    Args:
        manager: The TaskManager instance to add the task to
    """
    # Prompt for title
    console.print("[cyan]Enter task title:[/cyan] ", end="")
    title_input = input()
    title = sanitize_input(title_input)

    # Validate title
    error = validate_title(title)
    if error:
        console.print(f"❌ [bold red]Error:[/bold red] {error}\n", style="red")
        return

    # Prompt for description (optional)
    console.print("[cyan]Enter description (optional):[/cyan] ", end="")
    description_input = input()
    description = sanitize_input(description_input)

    # Validate description
    error = validate_description(description)
    if error:
        console.print(f"❌ [bold red]Error:[/bold red] {error}\n", style="red")
        return

    # Add task
    task = manager.add(title, description)

    # Success confirmation with task details
    task_info = f"[bold]Task #{task.id}[/bold]\n"
    task_info += f"Title: {task.title}\n"
    task_info += f"Description: {task.description if task.description else '(none)'}"

    console.print(
        Panel.fit(
            task_info,
            title="✅ [bold green]Task Added Successfully[/bold green]",
            border_style="green",
            padding=(1, 2)
        )
    )
    console.print()


def handle_exit() -> None:
    """Handle application exit with a beautiful goodbye message."""
    goodbye = Text()
    goodbye.append("\n👋 ", style="bold yellow")
    goodbye.append("Thanks for using Todo App!", style="bold cyan")
    goodbye.append("\n🚀 ", style="bold green")
    goodbye.append("Phase I Complete - Built with Claude Code", style="bold white")
    goodbye.append("\n✨ ", style="bold magenta")
    goodbye.append("Spec-Driven Development FTW!", style="bold yellow")

    console.print(
        Panel.fit(
            goodbye,
            border_style="cyan",
            padding=(1, 2),
            title="[bold cyan]Goodbye![/bold cyan]"
        )
    )


def main() -> None:
    """Entry point for the application."""
    main_loop()


if __name__ == "__main__":
    main()
