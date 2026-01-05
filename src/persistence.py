"""JSON persistence layer for task and config data.

This module handles saving and loading tasks to/from JSON files with
atomic writes and corruption recovery.
"""

import json
from pathlib import Path
from typing import List
from dataclasses import asdict
from datetime import datetime

from src.models import Task, Config


class DataStore:
    """Manages JSON persistence for tasks and configuration."""

    def __init__(self, data_file: str = ".todo-data.json"):
        """Initialize the data store.

        Args:
            data_file: Path to the task data JSON file
        """
        self.data_file = Path(data_file)
        self.backup_file = Path(f"{data_file}.backup")
        self.config_file = Path(".todo-config.json")

    def load_tasks(self) -> List[Task]:
        """Load tasks from JSON file.

        Returns:
            List of Task objects, empty list if file doesn't exist

        Handles:
            - Missing file: returns empty list
            - Corrupted JSON: restores from backup
            - Missing fields: uses dataclass defaults
        """
        if not self.data_file.exists():
            return []

        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)

            tasks = []
            for task_dict in data:
                # Parse datetime fields
                if 'created_at' in task_dict and task_dict['created_at']:
                    task_dict['created_at'] = datetime.fromisoformat(task_dict['created_at'])
                if 'updated_at' in task_dict and task_dict['updated_at']:
                    task_dict['updated_at'] = datetime.fromisoformat(task_dict['updated_at'])
                if 'completed_at' in task_dict and task_dict['completed_at']:
                    task_dict['completed_at'] = datetime.fromisoformat(task_dict['completed_at'])

                tasks.append(Task(**task_dict))

            return tasks

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            # Corrupted file - try to restore from backup
            if self.backup_file.exists():
                try:
                    self.backup_file.rename(self.data_file)
                    return self.load_tasks()  # Recursive call with restored file
                except Exception:
                    pass

            # If backup also fails, return empty list
            return []

    def save_tasks(self, tasks: List[Task]) -> None:
        """Save tasks to JSON file with atomic write.

        Args:
            tasks: List of Task objects to save

        Uses atomic write pattern:
            1. Backup current file (if exists)
            2. Write new data
            3. Delete backup on success
            4. Restore backup on failure
        """
        # Backup current file
        if self.data_file.exists():
            try:
                self.data_file.rename(self.backup_file)
            except Exception:
                pass  # Continue even if backup fails

        # Write new data
        try:
            data = []
            for task in tasks:
                task_dict = asdict(task)
                # Convert datetime objects to ISO format strings
                if task_dict['created_at']:
                    task_dict['created_at'] = task_dict['created_at'].isoformat()
                if task_dict['updated_at']:
                    task_dict['updated_at'] = task_dict['updated_at'].isoformat()
                if task_dict['completed_at']:
                    task_dict['completed_at'] = task_dict['completed_at'].isoformat()
                data.append(task_dict)

            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)

            # Success - remove backup
            if self.backup_file.exists():
                self.backup_file.unlink()

        except Exception as e:
            # Restore backup on failure
            if self.backup_file.exists():
                try:
                    self.backup_file.rename(self.data_file)
                except Exception:
                    pass
            raise  # Re-raise the original exception

    def load_config(self) -> Config:
        """Load user configuration from JSON file.

        Returns:
            Config object with user settings or defaults
        """
        if not self.config_file.exists():
            return Config()

        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
            return Config(**data)
        except (json.JSONDecodeError, KeyError):
            # Corrupted config - return defaults
            return Config()

    def save_config(self, config: Config) -> None:
        """Save user configuration to JSON file.

        Args:
            config: Config object to save
        """
        try:
            data = asdict(config)
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass  # Silent fail for config saves
