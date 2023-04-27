from sqlalchemy import delete, insert, select, update

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def select_all_filter_by(cls, **kwargs):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def select_all_filter_by_order_by(cls, filter_data: dict, order_data):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_data).order_by(order_data)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def select_one_or_none_filter_by(cls, **kwargs):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add_rows(cls, **kwargs):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**kwargs)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_rows_filer_by(cls, **kwargs):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**kwargs)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_rows_filter_by(cls, filter_by_dict, update_dict):
        async with async_session_maker() as session:
            query = update(cls.model).filter_by(**filter_by_dict).values(**update_dict)
            await session.execute(query)
            await session.commit()
