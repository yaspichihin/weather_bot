from aiogram import types

from app.answers.admin_answers import get_user_info
from app.users.models import Users


async def adm_main_menu():
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Список пользователей')
    btn2 = types.KeyboardButton('Основное меню')
    markup.add(btn1, btn2)
    return markup


async def adm_users_first_page(users: list[Users], page: int, total_pages: int):
    inline_markup = types.InlineKeyboardMarkup()
    for user in users[:page*4]:
        inline_markup.add(
            types.InlineKeyboardButton(
                text=await get_user_info(user),
                callback_data='None'
            )
        )
    page += 1
    inline_markup.row(
        types.InlineKeyboardButton(
            text=f'{page-1}/{total_pages}',
            callback_data='None'
        ),
        types.InlineKeyboardButton(
            text='Вперёд',
            callback_data=f'next_users_{page}'
        )
    )
    return inline_markup, page


async def adm_users_mid_page(users: list[Users], page: int, total_pages: int):
    inline_markup = types.InlineKeyboardMarkup()
    for user in users[page * 4 - 4:page * 4]:
        inline_markup.add(
            types.InlineKeyboardButton(
                text=await get_user_info(user),
                callback_data='None'
            )
        )
    page += 1
    inline_markup.row(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data=f'prev_users_{page - 2}'
        ),
        types.InlineKeyboardButton(
            text=f'{page - 1}/{total_pages}',
            callback_data='None'
        ),
        types.InlineKeyboardButton(
            text='Вперёд',
            callback_data=f'next_users_{page}'
        )
    )
    return inline_markup, page


async def adm_users_last_page(users: list[Users], page: int, total_pages: int):
    inline_markup = types.InlineKeyboardMarkup()
    for user in users[page * 4 - 4:len(users) + 1]:
        inline_markup.add(
            types.InlineKeyboardButton(
                text=await get_user_info(user),
                callback_data='None'
            )
        )
    page -= 1
    inline_markup.row(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data=f'prev_users_{page}'
        ),
        types.InlineKeyboardButton(
            text=f'{page + 1}/{total_pages}',
            callback_data='None'
        )
    )
    return inline_markup, page
