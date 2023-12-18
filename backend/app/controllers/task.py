from backend.app.models import Task
from backend.app.repositories import TaskRepository
from backend.core.database.transactional import Propagation, Transactional


class TaskController:
    """Task controller."""

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def get_by_author_id(self, author_id: int) -> list[Task]:
        """
        Returns a list of tasks based on author_id.

        :param author_id: The author id.
        :return: A list of tasks.
        """

        return self.task_repository.get_by_author_id(author_id)

    @Transactional(propagation=Propagation.REQUIRED)
    def add(self, title: str, description: str, author_id: int) -> Task:
        """
        Adds a task.

        :param title: The task title.
        :param description: The task description.
        :param author_id: The author id.
        :return: The task.
        """

        return self.task_repository.create(
            {
                "title": title,
                "description": description,
                "task_author_id": author_id,
            }
        )

    @Transactional(propagation=Propagation.REQUIRED)
    def complete(self, task_id: int) -> Task:
        """
        Completes a task.

        :param task_id: The task id.
        :return: The task.
        """

        task = self.task_repository.get_by_id(task_id)
        task.is_completed = True

        return task
