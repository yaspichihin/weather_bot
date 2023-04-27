from app.dao.base import BaseDAO
from app.reports.models import Reports
from app.users.dao import UsersDAO
from app.users.models import Users


class ReportsDAO(BaseDAO):
    model = Reports

    @classmethod
    async def add_report(cls, telegram_id: int, temp: int,
        feels_like: int, wind_speed: int, pressure_mm: int, city: str) -> None:
        user: Users = await UsersDAO.select_one_or_none_filter_by(tg_id=telegram_id)
        await cls.add_rows(user_id=user.id, temp=temp, feels_like=feels_like,
            wind_speed=wind_speed, pressure_mm=pressure_mm, city=city)

    @classmethod
    async def get_reports(cls, telegram_id: int) -> list[Reports]:
        user: Users = await UsersDAO.select_one_or_none_filter_by(tg_id=telegram_id)
        reports = await ReportsDAO.select_all_filter_by_order_by(
            {'user_id': user.id}, Reports.date.desc())
        return reports

    @classmethod
    async def del_report(cls, report_id: int) -> None:
        await ReportsDAO.delete_rows_filer_by(id=report_id)
