from pathlib import Path

import pytest

from task_manager.manager import TaskManager


def test_add_task() -> None:
    manager = TaskManager()

    task = manager.add_task("Learn pytest")

    assert task.id == 1
    assert task.title == "Learn pytest"
    assert task.completed is False


def test_empty_title_raises_error() -> None:
    manager = TaskManager()

    with pytest.raises(ValueError, match="cannot be empty"):
        manager.add_task("   ")


def test_complete_task() -> None:
    manager = TaskManager()
    task = manager.add_task("Learn Ruff")

    completed_task = manager.complete_task(task.id)

    assert completed_task.completed is True


def test_missing_task_raises_error() -> None:
    manager = TaskManager()

    with pytest.raises(KeyError, match="Task 99 not found"):
        manager.complete_task(99)


def test_save_and_load_tasks(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    manager = TaskManager()
    manager.add_task("Learn JSON")

    manager.save_to_json(file_path)
    loaded_manager = TaskManager.load_from_json(file_path)

    assert loaded_manager.list_tasks() == manager.list_tasks()


def test_corrupted_json_raises_error(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    file_path.write_text("{broken", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid task file"):
        TaskManager.load_from_json(file_path)
        