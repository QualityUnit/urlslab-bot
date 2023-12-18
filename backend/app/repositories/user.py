from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from backend.app.models import User


class UserRepository:
    """
    User repository provides all the database operations for the User model.
    """

    async def get_by_username(
            self, username: str, join_: set[str] | None = None
    ) -> User | None:
        """
        Get user by username.

        :param username: Username.
        :param join_: Join relations.
        :return: User.
        """
        return None

    async def get_by_email(
            self, email: str, join_: set[str] | None = None
    ) -> User | None:
        """
        Get user by email.

        :param email: Email.
        :param join_: Join relations.
        :return: User.
        """
        return None

    def _join_tasks(self, query: Select) -> Select:
        """
        Join tasks.

        :param query: Query.
        :return: Query.
        """
        return query.options(joinedload(User.tasks)).execution_options(
            contains_joined_collection=True
        )
