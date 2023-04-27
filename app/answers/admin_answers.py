from app.reports.dao import ReportsDAO
from app.reports.models import Reports
from app.users.models import Users


async def get_user_info(user: Users) -> str:
    reports: list[Reports] = await ReportsDAO.get_reports(user.tg_id)
    text = (
        f'ID: {user.firstname}. Подключился: '
        f'{user.connection_date.day}.'
        f'{user.connection_date.month}.'
        f'{user.connection_date.year}. '
        f'Отчётов: {len(reports)}'
    )
    return text
