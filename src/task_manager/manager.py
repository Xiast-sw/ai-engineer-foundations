import json
from dataclasses import asdict
from pathlib import Path

from .models import Task


class TaskManager:
    def __init__(self) -> None:
        self._tasks: list[Task] = []
        self._next_id = 1

    def add_task(self, title: str) -> Task:
        title = title.strip()

        if not title:
            raise ValueError("Task title cannot be empty.")

        task = Task(id=self._next_id, title=title)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def complete_task(self, task_id: int) -> Task:
        for task in self._tasks:
            if task.id == task_id:
                task.completed = True
                return task

        raise KeyError(f"Task {task_id} not found.")

    def list_tasks(self) -> list[Task]:
        return list(self._tasks)

    def save_to_json(self, path: str | Path) -> None:
        file_path = Path(path)
        data = [asdict(task) for task in self._tasks]
        file_path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load_from_json(cls, path: str | Path) -> "TaskManager":
        file_path = Path(path)

        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid task file: {file_path}") from error

        manager = cls()

        for item in data:
            manager._tasks.append(
                Task(
                    id=item["id"],
                    title=item["title"],
                    completed=item["completed"],
                )
            )

        manager._next_id = max(
            (task.id for task in manager._tasks),
            default=0,
        ) + 1

        return manager