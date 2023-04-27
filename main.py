import math

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.answers.main_answers import get_new_user_msg, get_query_msg
from app.answers.weather_answers import get_weather_answer
from app.config import settings
from app.markups.admin_markups import (
    adm_main_menu,
    adm_users_first_page,
    adm_users_last_page,
    adm_users_mid_page,
)
from app.markups.history_markups import (
    hist_first_page,
    hist_last_page,
    hist_mid_page,
    hist_none_report,
    hist_report,
)
from app.markups.main_markups import main_menu, menu_button
from app.reports.dao import ReportsDAO
from app.users.dao import UsersDAO
from app.users.models import Users
from app.yandex.geocode_api import get_city_name
from app.yandex.weather_api import get_weather


bot = Bot(token=settings.telegram_key)
# Записывать состояния в оперативную память, только для pet проектов.
# Для реальных проектов MongoDB, Redis. При перезапуске бота данные остаются.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Начало работы с ботом, пользователь ввел '/start'
@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    # Внесем информацию по пользователю в БД
    await UsersDAO.add_user(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.last_name
    )
    # Вернем первичное приветствие с меню из 4 кнопок
    text = get_new_user_msg(message.from_user.first_name)
    markup = await main_menu(message)
    await message.answer(text, reply_markup=markup)


# Пользователь нажал на кнопку или ввел текст 'Меню'
@dp.message_handler(regexp='Меню')
async def menu_message(message: types.Message):
    text = get_query_msg()
    markup = await main_menu(message)
    await message.answer(text, reply_markup=markup)


# Пользователь нажал на кнопку или ввел текст 'Погода в моём городе'
@dp.message_handler(regexp='Погода в моём городе')
async def get_weather_user_city(message: types.Message):
    # Шаблон ответа если город не установлен
    text = "(´｡•ᵕ•｡`) Город не задан.\n Закрепите желаемый город =)"
    # Получим установленный город пользователя
    city: str = await UsersDAO.get_city(message.from_user.id)
    # Если город установлен
    if city:
        # Шаблон ответа если geocoder не может распознать город
        text: str = (
                f"(｡•́︿•̀｡) Погода для города {city} не доступна.\n"
                "Переустановите город или повторить запрос позднее."
        )
        # Получим данные по погоде, если geocoder смог распознать город
        data: dict | None = get_weather(city)
        if data:
            # Добавим полученные данные о погоде в БД
            await ReportsDAO.add_report(
                message.from_user.id,
                data['fact']['temp'],
                data['fact']['feels_like'],
                data['fact']['wind_speed'],
                data['fact']['pressure_mm'],
                data['geo_object']['locality']['name']
            )
            # Формирование ответа
            text: str = get_weather_answer(
                data['geo_object']['locality']['name'],
                data['fact']['temp'],
                data['fact']['feels_like'],
                data['fact']['wind_speed'],
                data['fact']['pressure_mm']
            )
    markup = await menu_button()
    await message.answer(text, reply_markup=markup)


# Пользователь нажал на кнопку или ввел текст 'История'
@dp.message_handler(regexp='История')
async def get_user_history(message: types.Message):
    # Получим все отчеты пользователя
    reports = await ReportsDAO.get_reports(message.from_user.id)
    total_pages: int = math.ceil(len(reports) / 4)
    text = 'История запросов:'

    # Если отчеты пользователя не найдены
    if not reports:
        text: str = '(シ_ _)シ Запросы не найдены'
        markup = await menu_button()
        await message.answer(text, reply_markup=markup)
        return

    inline_markup, current_page = await hist_first_page(
        reports, 1, total_pages
    )
    await message.answer(text, reply_markup=inline_markup)


class ChoiceCityWeather(StatesGroup):
    # В переменной waiting_city как раз и будет храниться состояние диалога
    waiting_city = State()


# Пользователь нажал на кнопку или ввел текст 'Погода в другом месте'
@dp.message_handler(regexp='Погода в другом месте')
async def get_weather_other_city(message: types.Message):
    text = '(｡•̀ᴗ-)✧ Введите название города'
    markup = await menu_button()
    await message.answer(text, reply_markup=markup)
    await ChoiceCityWeather.waiting_city.set()


# В handler мы указываем на какое конкретно состояние он должен реагировать
# state: FSMContext необходим для того, чтобы мы могли записывать данные пользователя в память.
@dp.message_handler(state=ChoiceCityWeather.waiting_city)
async def city_chosen(message: types.Message, state: FSMContext):
    # Записываем введённый пользователем текст
    await state.update_data(waiting_city=message.text.capitalize())
    # Записываем в переменную введённые пользователем данные
    city = await state.get_data()
    # Получение данных по введённому городу от yandex api
    data: dict | None = get_weather(city.get('waiting_city'))
    # Ответ если город не найден
    text: str = "⊂(´ ▽ `)⊃ Город не найден, повторите попытку"
    # Если город найден
    if data:
        # Загрузка данных в БД
        await ReportsDAO.add_report(
            message.from_user.id,
            data['fact']['temp'],
            data['fact']['feels_like'],
            data['fact']['wind_speed'],
            data['fact']['pressure_mm'],
            data['geo_object']['locality']['name']
        )
        # Формирование ответа
        # Формирование ответа
        text: str = get_weather_answer(
            data['geo_object']['locality']['name'],
            data['fact']['temp'],
            data['fact']['feels_like'],
            data['fact']['wind_speed'],
            data['fact']['pressure_mm']
        )
    # Отправим ответ пользователю
    markup = await main_menu(message)
    await message.answer(text, reply_markup=markup)
    # Выводим диалог из состояния, т.е. он перестаёт записывать чего там пользователь пишет
    await state.finish()


class SetUserCity(StatesGroup):
    waiting_user_city = State()


# Пользователь нажал на кнопку или ввел текст 'Установить свой город'
@dp.message_handler(regexp='Установить свой город')
async def set_user_city(message: types.Message):
    text = 'Какой город закрепить?'
    markup = await menu_button()
    await message.answer(text, reply_markup=markup)
    await SetUserCity.waiting_user_city.set()


@dp.message_handler(state=SetUserCity.waiting_user_city)
async def city_chosen(message: types.Message, state: FSMContext):
    await state.update_data(waiting_user_city=message.text.capitalize())
    city = await state.get_data()
    # Ответ если город не найден
    text: str = "(｡•́︿•̀｡) Город не найден, повторите попытку"
    geocoder_city_name: str = get_city_name(city.get('waiting_user_city'))
    # Если город определен
    if geocoder_city_name:
        # Установить закрепленный городу пользователя в БД
        await UsersDAO.set_city(message.from_user.id, geocoder_city_name)
        text = f"Запомнил, {geocoder_city_name} ваш город"
    markup = await main_menu(message)
    await message.answer(text, reply_markup=markup)
    await state.finish()


@dp.message_handler(lambda message:
    message.from_user.id in settings.tg_bot_admin and
    message.text == 'Администратор'
)
async def admin_panel(message: types.Message):
    markup = await adm_main_menu()
    text = 'Переход в меню администратора'
    await message.answer(text=text, reply_markup=markup)


@dp.message_handler(lambda message:
    message.from_user.id in settings.tg_bot_admin and
    message.text == 'Список пользователей'
)
async def get_all_users(message: types.Message):
    users: list[Users] = await UsersDAO.get_all_users()
    total_pages = math.ceil(len(users) / 4)
    text = 'Все мои пользователи:'
    inline_markup, current_page = await adm_users_first_page(users, 1, total_pages)
    await message.answer(text, reply_markup=inline_markup)


# Заглушка выхода если получаем None
@dp.callback_query_handler(lambda call: call.data == 'None')
async def none_stun(call, state: FSMContext):
    return


# Навигация по меню истории, тут lambda с условием, чтобы не путать с другими каруселями
@dp.callback_query_handler(lambda call: 'users' not in call.data)
async def callback_query(call, state: FSMContext):
    # Получаем тип операции и номер страницы или отчета из callback_data
    query_type, query_id = call.data.split('_')
    async with state.proxy() as data:
        # Сохраняем страницу на которой находится пользователь в память
        data['current_page'] = int(query_id)
        await state.update_data(current_page=data['current_page'])
        reports = await ReportsDAO.get_reports(call.from_user.id)
        total_pages = math.ceil(len(reports) / 4)

        # Если пользователь нажал кнопку вперед
        if query_type == 'next':
            # Если страница последняя выдать шаблон последней страницы
            if data['current_page'] * 4 >= len(reports):
                inline_markup, data['current_page'] = await hist_last_page(
                    reports, data['current_page'], total_pages
                )
            # Иначе выдать шаблон средней страницы
            else:
                inline_markup, data['current_page'] = await hist_mid_page(
                    reports, data['current_page'], total_pages
                )
            await call.message.edit_text(
                text="История запросов:",
                reply_markup=inline_markup
            )
            return

        # Если пользователь нажал кнопку назад
        if query_type == 'prev':
            # Если страница первая выдать шаблон первой страницы
            if data['current_page'] == 1:
                inline_markup, data['current_page'] = await hist_first_page(
                    reports, data['current_page'], total_pages
                )
            # Иначе выдать шаблон средней страницы
            else:
                inline_markup, data['current_page'] = await hist_mid_page(
                    reports, data['current_page'], total_pages
                )
            await call.message.edit_text(
                text="История запросов:",
                reply_markup=inline_markup
            )
            return

        # Если пользователь нажал кнопку отчета
        if query_type == 'report':
            inline_markup, text = await hist_report(
                reports, data['current_page'], query_id)
            await call.message.edit_text(
                text=text,
                reply_markup=inline_markup
            )
            return

        # Если пользователь внутри отчета нажал кнопку "Назад"
        if query_type == 'return':
            inline_markup, data['current_page'] = await hist_first_page(
                reports, 1, total_pages
            )
            await call.message.edit_text(
                text='История запросов:',
                reply_markup=inline_markup
            )
            return

        # Если пользовать внутри отчета нажал кнопку "Удалить запрос"
        if query_type == 'delete':
            await ReportsDAO.del_report(int(query_id))
            reports = await ReportsDAO.get_reports(call.from_user.id)
            # Если отчеты еще есть
            if reports:
                inline_markup, data['current_page'] = await hist_first_page(
                    reports, 1, total_pages
                )
                await call.message.edit_text(
                    text='История запросов:',
                    reply_markup=inline_markup
                )
                return

            # Если отчеты пользователя не найдены
            inline_markup = await hist_none_report()
            await call.message.edit_text(
                text='История запросов:',
                reply_markup=inline_markup
            )
            return


# Навигация по меню пользователей, тут lambda с условием, чтобы не путать с другими каруселями
@dp.callback_query_handler(lambda call: 'users' in call.data)
async def callback_query(call, state: FSMContext):
    query_type, query_data, query_id = call.data.split('_')
    async with state.proxy() as data:
        data['current_page'] = int(query_id)
        await state.update_data(current_page=data['current_page'])
        users: list[Users] = await UsersDAO.get_all_users()
        total_pages = math.ceil(len(users) / 4)

        # Если пользователь нажал кнопку вперед
        if query_type == 'next':
            # Если страница последняя выдать шаблон последней страницы
            if data['current_page'] * 4 >= len(users):
                inline_markup, data['current_page'] = await adm_users_last_page(
                    users, data['current_page'], total_pages,
                )
            # Иначе выдать шаблон средней страницы
            else:
                inline_markup, data['current_page'] = await adm_users_mid_page(
                    users, data['current_page'], total_pages,
                )
            await call.message.edit_text(
                text='Все мои пользователи:',
                reply_markup=inline_markup,
            )
            return

        # Если пользователь нажал кнопку назад
        if query_type == 'prev':
            # Если страница первая выдать шаблон первой страницы
            if data['current_page'] == 1:
                inline_markup, data['current_page'] = await adm_users_first_page(
                    users, 1, total_pages
                )
            # Иначе выдать шаблон средней страницы
            else:
                inline_markup, data['current_page'] = await adm_users_mid_page(
                    users, data['current_page'], total_pages
                )
            await call.message.edit_text(
                text='Все мои пользователи:',
                reply_markup=inline_markup
            )
            return


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
