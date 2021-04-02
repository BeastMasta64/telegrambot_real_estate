from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message

from keyboards.inline.menu_keyboards import menu_cd, deal_type_keyboard, estate_type_keyboard, \
    estate_direction_keyboard, item_keyboard
from loader import dp
from utils.db_api.db_commands import get_item


# Хендлер на команду /menu
@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    # Выполним функцию, которая отправит пользователю кнопки с доступными типами сделок
    await list_deal_types(message)


# Та самая функция, которая отдает типы сделок. Она может принимать как CallbackQuery, так и Message
# Помимо этого, мы в нее можем отправить и другие параметры - estate_type, estate_direction
# Поэтому ловим все остальное в **kwargs
async def list_deal_types(message: Union[CallbackQuery, Message], **kwargs):
    # Клавиатуру формируем с помощью следующей функции (где делается запрос в базу данных)
    markup = await deal_type_keyboard()

    # Проверяем, что за тип апдейта. Если Message - отправляем новое сообщение
    if isinstance(message, Message):
        await message.answer("Смотри, что у нас есть", reply_markup=markup)

    # Если CallbackQuery - изменяем это сообщение
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


# Функция, которая отдает кнопки с типами недвижимости, по выбранной пользователем типу сделки
async def list_estate_types(callback: CallbackQuery, deal_type, dom, uchastok, townhouse, apartamenti, kvartira,
                            **kwargs):
    markup = await estate_type_keyboard(deal_type, dom, uchastok, townhouse, apartamenti, kvartira)

    # Изменяем сообщение, и отправляем новые кнопки с типами недвижимости
    await callback.message.edit_reply_markup(markup)


# Функция, которая отдает кнопки с направлениями недвижимости
async def list_estate_directions(callback: CallbackQuery, deal_type, dom, uchastok, townhouse, apartamenti, kvartira,
                                 novorijskoe, rublevskoe,
                                 kievskoe, dmitrovskoe, rublevo_uspenskoe, minskoe, ilinskoe, kalujskoe, borovskoe,
                                 vtoroe_uspenskoe, **kwargs):
    markup = await estate_direction_keyboard(deal_type, dom, uchastok, townhouse, apartamenti, kvartira, novorijskoe,
                                             rublevskoe,
                                             kievskoe, dmitrovskoe, rublevo_uspenskoe, minskoe, ilinskoe, kalujskoe,
                                             borovskoe,
                                             vtoroe_uspenskoe)

    # Изменяем сообщение, и отправляем новые кнопки с направлениями
    await callback.message.edit_text(text="Смотри, что у нас есть", reply_markup=markup)


# Функция, которая отдает кнопки с направлениями недвижимости
async def list_estate_directions(callback: CallbackQuery, deal_type, dom, uchastok, townhouse, apartamenti, kvartira,
                                 novorijskoe, rublevskoe,
                                 kievskoe, dmitrovskoe, rublevo_uspenskoe, minskoe, ilinskoe, kalujskoe, borovskoe,
                                 vtoroe_uspenskoe, **kwargs):
    markup = await estate_direction_keyboard(deal_type, dom, uchastok, townhouse, apartamenti, kvartira, novorijskoe,
                                             rublevskoe,
                                             kievskoe, dmitrovskoe, rublevo_uspenskoe, minskoe, ilinskoe, kalujskoe,
                                             borovskoe,
                                             vtoroe_uspenskoe)

    # Изменяем сообщение, и отправляем новые кнопки с направлениями
    await callback.message.edit_text(text="Смотри, что у нас есть", reply_markup=markup)


# # Функция, которая отдает уже кнопку Купить товар по выбранному товару
# async def show_item(callback: CallbackQuery, category, subcategory, item_id):
#     markup = item_keyboard(category, subcategory, item_id)
#
#     # Берем запись о нашем товаре из базы данных
#     item = await get_item(item_id)
#     text = f"Купи {item.name}"
#     await callback.message.edit_text(text=text, reply_markup=markup)


# Функция, которая обрабатывает ВСЕ нажатия на кнопки в этой менюшке
@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """

    :param call: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    """

    # Получаем текущий уровень меню, который запросил пользователь
    current_level = callback_data.get("level")

    # Получаем тип сделки, которую выбрал пользователь (Передается всегда)
    deal_type = callback_data.get("deal_type")

    estate_types = {
        # Получаем выбор дома(True или False)
        'dom': callback_data.get("dom"),
        # Получаем выбор участка(True или False)
        'uchastok': callback_data.get("uchastok"),
        # Получаем выбор таунхауса(True или False)
        'townhouse': callback_data.get("townhouse"),
        # Получаем выбор апртаменты(True или False)
        'apartamenti': callback_data.get("apartamenti"),
        # Получаем выбор квартира(True или False)
        'kvartira': callback_data.get("kvartira")
    }
    # Получаем тип недвижимости, которую выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    estate_type = callback_data.get("estate_type")
    # Если была нажата кнопка с конкретным типом недвижимости, меняем ее значение на обратное
    try:
        estate_types[estate_type] = not estate_types[estate_type]
    except KeyError:
        pass

    estate_directions = {
        # Получаем выбор новорижского направления(True или False)
        'novorijskoe': callback_data.get("novorijskoe"),
        # Получаем выбор рублевского направления(True или False)
        'rublevskoe': callback_data.get("rublevskoe"),
        # Получаем выбор киевского направления(True или False)
        'kievskoe': callback_data.get("kievskoe"),
        # Получаем выбор дмитровского направления(True или False)
        'dmitrovskoe': callback_data.get("dmitrovskoe"),
        # Получаем выбор рублево-успенского направления(True или False)
        'rublevo_uspenskoe': callback_data.get("rublevo_uspenskoe"),
        # Получаем выбор минского направления(True или False)
        'minskoe': callback_data.get("minskoe"),
        # Получаем выбор ильинского направления(True или False)
        'ilinskoe': callback_data.get("ilinskoe"),
        # Получаем выбор калужского направления(True или False)
        'kalujskoe': callback_data.get("kalujskoe"),
        # Получаем выбор боровского направления(True или False)
        'borovskoe': callback_data.get("borovskoe"),
        # Получаем выбор второе-успенского направления(True или False)
        'vtoroe_uspenskoe': callback_data.get("vtoroe_uspenskoe")
    }
    # Получаем направление недвижимости, который выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    estate_direction = callback_data.get("estate_direction")
    # Если была нажата кнопка с конкретным типом недвижимости, меняем ее значение на обратное
    try:
        estate_directions[estate_direction] = not estate_directions[estate_direction]
    except KeyError:
        pass

    # Прописываем "уровни" в которых будут отправляться новые кнопки пользователю
    levels = {
        "0": list_deal_types,  # Отдаем типы сделок
        "1": list_estate_types,  # Отдаем типы недвижиммости
        "2": list_estate_directions,  # Отдаем направления
        "3": show_item  # Предлагаем купить товар
    }

    # Забираем нужную функцию для выбранного уровня
    current_level_function = levels[current_level]

    # Выполняем нужную функцию и передаем туда параметры, полученные из кнопки
    await current_level_function(
        call,
        deal_type=deal_type,
        dom=estate_types['dom'],
        uchastok=estate_types['uchastok'],
        townhouse=estate_types['townhouse'],
        apartamenti=estate_types['apartamenti'],
        kvartira=estate_types['kvartira'],
        novorijskoe=estate_directions['novorijskoe'],
        rublevskoe=estate_directions['rublevskoe'],
        kievskoe=estate_directions['kievskoe'],
        dmitrovskoe=estate_directions['dmitrovskoe'],
        rublevo_uspenskoe=estate_directions['rublevo_uspenskoe'],
        minskoe=estate_directions['minskoe'],
        ilinskoe=estate_directions['ilinskoe'],
        kalujskoe=estate_directions['kalujskoe'],
        borovskoe=estate_directions['borovskoe'],
        vtoroe_uspenskoe=estate_directions['vtoroe_uspenskoe']
    )
