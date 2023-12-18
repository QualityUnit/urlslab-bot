from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from backend.app.models import Task


class TaskRepository:
    """
    Task repository provides all the database operations for the Task model.
    """

    def get_by_author_id(
        self, author_id: int, join_: set[str] | None = None
    ) -> list[Task]:
        """
        Get all tasks by author id.

        :param author_id: The author id to match.
        :param join_: The joins to make.
        :return: A list of tasks.
        """
        return []

    def _join_author(self, query: Select) -> Select:
        """
        Join the author relationship.

        :param query: The query to join.
        :return: The joined query.
        """
        return query.options(joinedload(Task.author))
