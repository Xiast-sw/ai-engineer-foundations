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