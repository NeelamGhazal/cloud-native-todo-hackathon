"""Main CLI interface for the todo application.

This module provides the command-line interface and entry point for the application.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

from src.operations import TaskManager
from src.validators import (
    sanitize_input, validate_title, validate_description, validate_task_id,
    validate_priority, validate_tags, parse_tags, normalize_priority
)
from src.filters import filter_by_status, filter_by_priority, filter_by_tag, search_tasks, sort_tasks
from src.persistence import DataStore

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
    ║                   Spec-Driven Development                    ║
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
    # Initialize the task manager with persistence
    data_store = DataStore()
    manager = TaskManager(data_store)

    # Show banner
    show_banner()

    # Show loaded tasks message
    if len(manager.tasks) > 0:
        console.print(f"[dim cyan]📂 Loaded {len(manager.tasks)} task(s) from previous session[/dim cyan]\n")

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
            elif command == "/search":
                handle_search(manager)
            elif command == "/stats":
                handle_stats(manager)
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

    table.add_row("/add", "Add a new task (with priority and tags)")
    table.add_row("/list", "View all tasks")
    table.add_row("/search", "Search tasks by keyword")
    table.add_row("/stats", "Show task statistics")
    table.add_row("/complete", "Toggle task completion status")
    table.add_row("/update", "Update task details (title, desc, priority, tags)")
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

    # Create beautiful table with priority and tags
    table = Table(
        title="📋 [bold cyan]Your Tasks[/bold cyan]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold",
        border_style="cyan",
        expand=False
    )

    table.add_column("ID", style="bold cyan", justify="center", width=4)
    table.add_column("Status", justify="center", width=6)
    table.add_column("Priority", justify="center", width=8)
    table.add_column("Title", style="yellow", width=25)
    table.add_column("Description", style="white", width=30)
    table.add_column("Tags", style="magenta", width=15)

    # Print each task
    for task in tasks:
        # Status indicator with color
        status = "[bold green]✅[/bold green]" if task.completed else "[bold red]❌[/bold red]"

        # Priority with color and emoji
        priority_colors = {"High": "red", "Medium": "yellow", "Low": "green"}
        priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        p_color = priority_colors.get(task.priority, "white")
        p_emoji = priority_emoji.get(task.priority, "⚪")
        priority_display = f"[{p_color}]{p_emoji}[/{p_color}]"

        # Truncate title and description
        title_display = task.title[:25]
        if len(task.title) > 25:
            title_display = task.title[:22] + "..."

        description_display = task.description[:30] if task.description else ""
        if len(task.description) > 30:
            description_display = task.description[:27] + "..."

        # Format tags
        tags_display = ", ".join(task.tags[:2]) if task.tags else ""
        if len(task.tags) > 2:
            tags_display += f" +{len(task.tags) - 2}"

        # Add row to table
        table.add_row(
            str(task.id),
            status,
            priority_display,
            title_display,
            description_display,
            tags_display
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

    # Ask if user wants to update priority
    console.print("[cyan]Update priority? (y/n):[/cyan] ", end="")
    update_priority_input = input().strip().lower()
    new_priority = None
    if update_priority_input == "y":
        console.print("[cyan]Enter new priority (High/Medium/Low):[/cyan] ", end="")
        priority_input = input().strip()
        new_priority = normalize_priority(priority_input)

        # Validate priority
        error = validate_priority(new_priority)
        if error:
            console.print(f"❌ [bold red]Error:[/bold red] {error}\n", style="red")
            return

    # Ask if user wants to update tags
    console.print("[cyan]Update tags? (y/n):[/cyan] ", end="")
    update_tags_input = input().strip().lower()
    new_tags = None
    if update_tags_input == "y":
        console.print("[cyan]Enter new tags (comma-separated):[/cyan] ", end="")
        tags_input = input().strip()
        new_tags = parse_tags(tags_input) if tags_input else []

        # Validate tags
        if new_tags:
            error = validate_tags(new_tags)
            if error:
                console.print(f"❌ [bold red]Error:[/bold red] {error}\n", style="red")
                return

    # Check if at least one field is selected
    if new_title is None and new_description is None and new_priority is None and new_tags is None:
        console.print("❌ [bold red]Error:[/bold red] No fields selected for update\n", style="red")
        return

    # Update task
    updated_task = manager.update(task_id, title=new_title, description=new_description,
                                  priority=new_priority, tags=new_tags)

    # Success confirmation with task details
    priority_colors = {"High": "red", "Medium": "yellow", "Low": "green"}
    priority_color = priority_colors.get(updated_task.priority, "white")

    task_info = f"[bold]Task #{updated_task.id}[/bold]\n"
    task_info += f"Title: {updated_task.title}\n"
    task_info += f"Description: {updated_task.description}\n"
    task_info += f"Priority: [{priority_color}]{updated_task.priority}[/{priority_color}]\n"
    task_info += f"Tags: {', '.join(updated_task.tags) if updated_task.tags else '(none)'}"

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


def handle_search(manager: TaskManager) -> None:
    """Handle searching tasks by keyword.

    Args:
        manager: The TaskManager instance to search tasks in
    """
    # Prompt for keyword
    console.print("[cyan]Enter search keyword:[/cyan] ", end="")
    keyword_input = input()
    keyword = sanitize_input(keyword_input)

    # Validate keyword
    if not keyword:
        console.print("❌ [bold red]Error:[/bold red] Search keyword cannot be empty\\n", style="red")
        return

    # Search tasks
    all_tasks = manager.get_all()
    matching_tasks = search_tasks(all_tasks, keyword)

    # Check if any matches found
    if not matching_tasks:
        console.print(
            Panel.fit(
                f"🔍 [yellow]No tasks found matching '[bold]{keyword}[/bold]'[/yellow]",
                border_style="yellow",
                padding=(1, 2)
            )
        )
        console.print()
        return

    # Display results count
    console.print(f"[dim cyan]Found {len(matching_tasks)} task(s) matching '{keyword}'[/dim cyan]\\n")

    # Create results table
    table = Table(
        title=f"🔍 [bold cyan]Search Results: '{keyword}'[/bold cyan]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold",
        border_style="cyan",
        expand=False
    )

    table.add_column("ID", style="bold cyan", justify="center", width=4)
    table.add_column("Status", justify="center", width=6)
    table.add_column("Priority", justify="center", width=8)
    table.add_column("Title", style="yellow", width=25)
    table.add_column("Description", style="white", width=30)
    table.add_column("Tags", style="magenta", width=15)

    # Print each matching task
    for task in matching_tasks:
        # Status indicator with color
        status = "[bold green]✅[/bold green]" if task.completed else "[bold red]❌[/bold red]"

        # Priority with color and emoji
        priority_colors = {"High": "red", "Medium": "yellow", "Low": "green"}
        priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        p_color = priority_colors.get(task.priority, "white")
        p_emoji = priority_emoji.get(task.priority, "⚪")
        priority_display = f"[{p_color}]{p_emoji}[/{p_color}]"

        # Truncate title and description
        title_display = task.title[:25]
        if len(task.title) > 25:
            title_display = task.title[:22] + "..."

        description_display = task.description[:30] if task.description else ""
        if len(task.description) > 30:
            description_display = task.description[:27] + "..."

        # Format tags
        tags_display = ", ".join(task.tags[:2]) if task.tags else ""
        if len(task.tags) > 2:
            tags_display += f" +{len(task.tags) - 2}"

        # Add row to table
        table.add_row(
            str(task.id),
            status,
            priority_display,
            title_display,
            description_display,
            tags_display
        )

    console.print(table)
    console.print()


def handle_stats(manager: TaskManager) -> None:
    """Handle displaying task statistics.

    Args:
        manager: The TaskManager instance to get statistics from
    """
    # Get statistics
    stats = manager.get_statistics()

    # Check if there are any tasks
    if stats["total"] == 0:
        console.print(
            Panel.fit(
                "📊 [yellow]No tasks yet. Add one with[/yellow] [bold cyan]/add[/bold cyan]",
                border_style="yellow",
                padding=(1, 2)
            )
        )
        console.print()
        return

    # Create statistics display
    stats_table = Table(
        title="📊 [bold cyan]Task Statistics[/bold cyan]",
        box=box.DOUBLE,
        show_header=False,
        border_style="cyan",
        expand=False,
        width=60
    )

    stats_table.add_column("Metric", style="bold white", width=25)
    stats_table.add_column("Value", style="bold yellow", width=30)

    # Overall stats
    stats_table.add_row("Total Tasks", f"{stats['total']}")
    stats_table.add_row("Completed", f"[green]{stats['completed']} ✅[/green]")
    stats_table.add_row("Incomplete", f"[red]{stats['incomplete']} ❌[/red]")
    stats_table.add_row("Completion Rate", f"[cyan]{stats['completion_rate']:.1f}%[/cyan]")

    # Add separator
    stats_table.add_row("", "")

    # Priority breakdown
    stats_table.add_row("[bold]By Priority:[/bold]", "")
    stats_table.add_row("  🔴 High", f"{stats['by_priority']['High']}")
    stats_table.add_row("  🟡 Medium", f"{stats['by_priority']['Medium']}")
    stats_table.add_row("  🟢 Low", f"{stats['by_priority']['Low']}")

    console.print(stats_table)
    console.print()


def handle_add(manager: TaskManager) -> None:
    """Handle adding a new task with enhanced metadata.

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

    # Prompt for priority (optional)
    console.print("[cyan]Enter priority (High/Medium/Low, default: Medium):[/cyan] ", end="")
    priority_input = input().strip()
    priority = normalize_priority(priority_input) if priority_input else "Medium"

    # Prompt for tags (optional)
    console.print("[cyan]Enter tags (comma-separated, optional):[/cyan] ", end="")
    tags_input = input().strip()
    tags = parse_tags(tags_input) if tags_input else []

    # Validate tags
    if tags:
        error = validate_tags(tags)
        if error:
            console.print(f"❌ [bold red]Error:[/bold red] {error}\n", style="red")
            return

    # Add task
    task = manager.add(title, description, priority, tags)

    # Success confirmation with task details
    priority_colors = {"High": "red", "Medium": "yellow", "Low": "green"}
    priority_color = priority_colors.get(priority, "white")

    task_info = f"[bold]Task #{task.id}[/bold]\n"
    task_info += f"Title: {task.title}\n"
    task_info += f"Description: {task.description if task.description else '(none)'}\n"
    task_info += f"Priority: [{priority_color}]{task.priority}[/{priority_color}]\n"
    task_info += f"Tags: {', '.join(task.tags) if task.tags else '(none)'}"

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
