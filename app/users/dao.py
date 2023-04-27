from app.dao.base import BaseDAO
from app.users.models import Users


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def add_user(cls, telegram_id: int, firstname: str, lastname: str) -> None:
        if not await cls.select_one_or_none_filter_by(tg_id=telegram_id):
            await cls.add_rows(tg_id=telegram_id, firstname=firstname, lastname=lastname)

    @classmethod
    async def set_city(cls, telegram_id: int, user_city: str) -> None:
        await cls.update_rows_filter_by({'tg_id': telegram_id}, {'city': user_city})

    @classmethod
    async def get_city(cls, telegram_id: int):
        user: Users = await cls.select_one_or_none_filter_by(tg_id=telegram_id)
        return user.city

    @classmethod
    async def get_all_users(cls):
        users: list[Users] = await cls.select_all_filter_by()
        return users
