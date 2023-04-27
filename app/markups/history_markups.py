from aiogram import types

from app.answers.weather_answers import get_report_answer


async def hist_first_page(reports, page: int, total_pages: int):
    inline_markup = types.InlineKeyboardMarkup()
    for report in reports[0:page * 4]:
        inline_markup.add(
            types.InlineKeyboardButton(
                text=f'{report.city} {report.date.day}.{report.date.month}.{report.date.year}',
                callback_data=f'report_{report.id}'
            )
        )
    page += 1
    inline_markup.row(
        types.InlineKeyboardButton(
            text=f'{page - 1}/{total_pages}',
            callback_data='None'
        ),
        types.InlineKeyboardButton(
            text='Вперёд',
            callback_data=f'next_{page}'
        )
    )
    return inline_markup, page


async def hist_mid_page(reports, page: int, total_pages: int):
    inline_markup = types.InlineKeyboardMarkup()
    for report in reports[page*4 - 4:page*4]:
        inline_markup.add(
            types.InlineKeyboardButton(
                text=f'{report.city} {report.date.day}.{report.date.month}.{report.date.year}',
                callback_data=f'report_{report.id}'
            )
        )
    page += 1
    inline_markup.row(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data=f'prev_{page - 2}'
        ),
        types.InlineKeyboardButton(
            text=f'{page - 1}/{total_pages}',
            callback_data='None'
        ),
        types.InlineKeyboardButton(
            text='Вперёд',
            callback_data=f'next_{page}'
        )
    )
    return inline_markup, page


async def hist_last_page(reports, page: int, total_pages: int):
    inline_markup = types.InlineKeyboardMarkup()
    for report in reports[page * 4 - 4:len(reports) + 1]:
        inline_markup.add(
            types.InlineKeyboardButton(
                text=f'{report.city} {report.date.day}.{report.date.month}.{report.date.year}',
                callback_data=f'report_{report.id}'
            )
        )
    page -= 1
    inline_markup.row(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data=f'prev_{page}'
        ),
        types.InlineKeyboardButton(
            text=f'{page + 1}/{total_pages}',
            callback_data='None'
        )
    )
    return inline_markup, page


async def hist_report(reports, page: int, report_id: int):
    inline_markup = types.InlineKeyboardMarkup()
    # TODO: Подумать чем заменить линейный поиск
    for report in reports:
        if report.id == int(report_id):
            inline_markup.add(
                types.InlineKeyboardButton(
                    text='Назад',
                    callback_data=f'return_{page}'
                ),
                types.InlineKeyboardButton(
                    text='Удалить зарос',
                    callback_data=f'delete_{report_id}'
                )
            )
            text = get_report_answer(
                report.city,
                report.temp,
                report.feels_like,
                report.wind_speed,
                report.pressure_mm
            )
            return inline_markup, text


async def hist_none_report():
    text: str = 'Запросы не найдены (シ_ _)シ'
    inline_markup = types.InlineKeyboardMarkup()
    inline_markup.add(
        types.InlineKeyboardButton(
            text=text,
            callback_data='None'
        )
    )
    return inline_markup
