from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api.db_commands import get_estate_type, count_estates, get_items, get_deal_type, get_estate_direction, \
    get_estate_otdelka

# Создаем CallbackData-объекты, которые будут нужны для работы с менюшкой
menu_cd = CallbackData("show_menu", "level", "deal_type", "estate_type", 'dom', 'uchastok',
                       'townhouse', 'apartamenti', 'kvartira', "estate_direction", 'Novorijskoe', 'Rublevskoe',
                       'Kievskoe', 'Dmitrovskoe', 'Rublev-uspenskoe', 'Minskoe', 'Ilinskoe', 'Kalujskoe', 'Borovskoe',
                       'Vtoroe-uspenskoe', 'otdelka',
                       'how_far', 'ploshad_doma', 'ploshad_uchastka', 'floors', 'spalni', 'show_first')
buy_item = CallbackData("buy", "item_id")
direction_menu = CallbackData('direction')


# С помощью этой функции будем формировать коллбек дату для каждого элемента меню, в зависимости от
# переданных параметров. Если параметры не выбраны - они по умолчанию равны нулю или False
def make_callback_data(level, deal_type="0", estate_type="0", dom=False, uchastok=False,
                       townhouse=False, apartamenti=False, kvartira=False, estate_direction="0", novorijskoe=False,
                       rublevskoe=False, kievskoe=False, dmitrovskoe=False,
                       rublevo_uspenskoe=False, minskoe=False, ilinskoe=False, kalujskoe=False, borovskoe=False,
                       vtoroe_uspenskoe=False, otdelka="0", how_far="0",
                       ploshad_doma="0",
                       ploshad_uchastka="0", floors="0", spalni="0", show_first="0"):
    # Возвращаем сформированную колбек дату
    return menu_cd.new(level=level, deal_type=deal_type, estate_type=estate_type, dom=dom, uchastok=uchastok,
                       townhouse=townhouse, apartamenti=apartamenti, kvartira=kvartira,
                       estate_direction=estate_direction, novorijskoe=novorijskoe,
                       rublevskoe=rublevskoe, kievskoe=kievskoe, dmitrovskoe=dmitrovskoe,
                       rublevo_uspenskoe=rublevo_uspenskoe, minskoe=minskoe, ilinskoe=ilinskoe, kalujskoe=kalujskoe,
                       borovskoe=borovskoe,
                       vtoroe_uspenskoe=vtoroe_uspenskoe, otdelka=otdelka, how_far=how_far, ploshad_doma=ploshad_doma,
                       ploshad_uchastka=ploshad_uchastka, floors=floors, spalni=spalni, show_first=show_first)


# Создаем функцию, которая отдает клавиатуру с доступными типами сделок
async def deal_type_keyboard():
    # Указываем, что текущий уровень меню - 0
    CURRENT_LEVEL = 0

    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup()

    # Забираем список типов сделок из базы данных
    types = await get_deal_type()
    # Проходимся циклом по доступным нам типам сделок
    for type in types:
        # Чекаем в базе сколько недвижимости существует под данным типом сделки
        number_of_estates = await count_estates(type.deal_type)

        # Сформируем текст, который будет на кнопке
        button_text = f"{type.deal_type} ({number_of_estates} шт)"

        # Сформируем колбек дату, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем типы сделок
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, deal_type=type.deal_type)

        # Вставляем кнопку в клавиатуру
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Возвращаем созданную клавиатуру в хендлер
    return markup


# Создаем функцию, которая отдает клавиатуру с доступными типами недвижимости, исходя из выбранного типа сделки.
# Ее мы будем вызывать не единожды, так как пользователю будет предоставлена возможность кнопками выбрать несколько
# типов недвижимости
async def estate_type_keyboard(deal_type, dom, uchastok, townhouse, apartamenti, kvartira):
    # Текущий уровень - 1
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()

    # Забираем список недвижимости из базы данных с учетом выбранного типа сделки и проходим по ним
    estate_types = await get_estate_type(deal_type)
    for estate_type in estate_types:
        # Чекаем в базе сколько недвижости есть с учетом выбранных условий
        number_of_estate_types = await count_estates(deal_type=deal_type,
                                                     estate_type=estate_type.estate_type)

        # Сформируем текст, который будет на кнопке
        button_text = f"{estate_type.estate_type} ({number_of_estate_types} шт)"

        # Проверяем - выбрал ли пользователь этот тип недвижимости, если выбрал, то в тексте на кнопке с типом
        # недвижимости будет стоять пометка "да"
        check = eval(estate_type.estate_type)
        if check:
            button_text += ', да'

        # Сформируем колбек дату, которая будет на кнопке
        callback_data = make_callback_data(level=CURRENT_LEVEL,
                                           deal_type=deal_type, estate_type=estate_type.estate_type, dom=dom,
                                           uchastok=uchastok, townhouse=townhouse, apartamenti=apartamenti,
                                           kvartira=kvartira)
        # Вставляем кнопку в клавиатуру
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 0.
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1))
    )
    # Создаем Кнопку "Вперед", в которой прописываем колбек дату такую,
    # которая кидает пользователя на уровень вперед - на уровень 2.
    markup.row(
        InlineKeyboardButton(
            text='Далее',
            callback_data=make_callback_data(level=CURRENT_LEVEL + 1, dom=dom,
                                             uchastok=uchastok, townhouse=townhouse, apartamenti=apartamenti,
                                             kvartira=kvartira))
    )
    return markup


# Создаем функцию, которая отдает клавиатуру с доступными направлениями, исходя из входных данных
async def estate_direction_keyboard(deal_type, dom, uchastok, townhouse, apartamenti, kvartira, novorijskoe, rublevskoe,
                                    kievskoe, dmitrovskoe, rublevo_uspenskoe, minskoe, ilinskoe, kalujskoe, borovskoe,
                                    vtoroe_uspenskoe):
    CURRENT_LEVEL = 2
    # Устанавливаю row_width = 1, чтобы показывалась одна кнопка в строке на направление
    markup = InlineKeyboardMarkup(row_width=1)
    # Забираем список направлений из базы данных и проходим по нему
    directions = await get_estate_direction(deal_type, dom, uchastok, townhouse, apartamenti, kvartira)
    for direction in directions:
        # Сформируем колбек дату, которая будет на кнопке
        button_text = f'{direction.estate_direction}'
        # Проверяем - выбрал ли пользователь этот тип недвижимости, если выбрал, то в тексте на кнопке с типом
        # недвижимости будет стоять пометка "да"
        check = eval(direction.estate_direction)
        if check:
            button_text += ', да'

        # Сформируем колбек дату, которая будет на кнопке
        callback_data = make_callback_data(level=CURRENT_LEVEL,
                                           deal_type=deal_type, dom=dom,
                                           uchastok=uchastok, townhouse=townhouse, apartamenti=apartamenti,
                                           kvartira=kvartira,
                                           estate_direction=direction.estate_direction, novorijskoe=novorijskoe,
                                           rublevskoe=rublevskoe, kievskoe=kievskoe, dmitrovskoe=dmitrovskoe,
                                           rublevo_uspenskoe=rublevo_uspenskoe, minskoe=minskoe, ilinskoe=ilinskoe,
                                           kalujskoe=kalujskoe,
                                           borovskoe=borovskoe,
                                           vtoroe_uspenskoe=vtoroe_uspenskoe)
        # Вставляем кнопку в клавиатуру
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 1.
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             deal_type=deal_type, dom=dom,
                                             uchastok=uchastok, townhouse=townhouse, apartamenti=apartamenti,
                                             kvartira=kvartira))
    )
    # Создаем Кнопку "Вперед", в которой прописываем колбек дату такую,
    # которая кидает пользователя на уровень вперед - на уровень 2.
    markup.row(
        InlineKeyboardButton(
            text='Далее',
            callback_data=make_callback_data(level=CURRENT_LEVEL + 1, dom=dom,
                                             uchastok=uchastok, townhouse=townhouse, apartamenti=apartamenti,
                                             kvartira=kvartira, novorijskoe=novorijskoe,
                                             rublevskoe=rublevskoe, kievskoe=kievskoe, dmitrovskoe=dmitrovskoe,
                                             rublevo_uspenskoe=rublevo_uspenskoe, minskoe=minskoe, ilinskoe=ilinskoe,
                                             kalujskoe=kalujskoe,
                                             borovskoe=borovskoe,
                                             vtoroe_uspenskoe=vtoroe_uspenskoe))
    )
    return markup


# Создаем функцию, которая отдает клавиатуру с доступными отделками, исходя из входных данных
async def estate_otdelka_keyboard(deal_type, dom, uchastok, townhouse, apartamenti, kvartira, novorijskoe, rublevskoe,
                                  kievskoe, dmitrovskoe, rublevo_uspenskoe, minskoe, ilinskoe, kalujskoe, borovskoe,
                                  vtoroe_uspenskoe, bez_otdelki, pod_kluch, pod_otdelku):
    CURRENT_LEVEL = 3
    # Устанавливаю row_width = 1, чтобы показывалась одна кнопка в строке на направление
    markup = InlineKeyboardMarkup(row_width=1)
    # Забираем список отделок из базы данных и проходим по нему
    otdelki = await get_estate_otdelka(deal_type, dom, uchastok, townhouse, apartamenti, kvartira, novorijskoe,
                                       rublevskoe,
                                       kievskoe, dmitrovskoe, rublevo_uspenskoe, minskoe, ilinskoe, kalujskoe,
                                       borovskoe,
                                       vtoroe_uspenskoe)
    for otdelka in otdelki:
        # Сформируем колбек дату, которая будет на кнопке
        button_text = f'{otdelka.otdelka}'
        # Проверяем - выбрал ли пользователь эту отделку, если выбрал, то в тексте на кнопке с отделкой
        # будет стоять пометка "да"
        check = eval(otdelka.otdelka)
        if check:
            button_text += ', да'
        # Сформируем колбек дату, которая будет на кнопке
        callback_data = make_callback_data(level=CURRENT_LEVEL,
                                           deal_type=deal_type, dom=dom,
                                           uchastok=uchastok, townhouse=townhouse, apartamenti=apartamenti,
                                           kvartira=kvartira, novorijskoe=novorijskoe,
                                           rublevskoe=rublevskoe, kievskoe=kievskoe, dmitrovskoe=dmitrovskoe,
                                           rublevo_uspenskoe=rublevo_uspenskoe, minskoe=minskoe, ilinskoe=ilinskoe,
                                           kalujskoe=kalujskoe,
                                           borovskoe=borovskoe,
                                           vtoroe_uspenskoe=vtoroe_uspenskoe, otdelka=otdelka.otdelka,
                                           bez_otdelki=bez_otdelki,
                                           pod_kluch=pod_kluch, pod_otdelku=pod_otdelku)
        # Вставляем кнопку в клавиатуру
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 2.
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1, novorijskoe=novorijskoe,
                                             rublevskoe=rublevskoe, kievskoe=kievskoe, dmitrovskoe=dmitrovskoe,
                                             rublevo_uspenskoe=rublevo_uspenskoe, minskoe=minskoe, ilinskoe=ilinskoe,
                                             kalujskoe=kalujskoe,
                                             borovskoe=borovskoe,
                                             vtoroe_uspenskoe=vtoroe_uspenskoe))
    )
    # Создаем Кнопку "Вперед", в которой прописываем колбек дату такую,
    # которая кидает пользователя на уровень вперед - на уровень 2.
    markup.row(
        InlineKeyboardButton(
            text='Далее',
            callback_data=make_callback_data(level=CURRENT_LEVEL + 1, dom=dom,
                                             uchastok=uchastok, townhouse=townhouse, apartamenti=apartamenti,
                                             kvartira=kvartira, novorijskoe=novorijskoe,
                                             rublevskoe=rublevskoe, kievskoe=kievskoe, dmitrovskoe=dmitrovskoe,
                                             rublevo_uspenskoe=rublevo_uspenskoe, minskoe=minskoe, ilinskoe=ilinskoe,
                                             kalujskoe=kalujskoe,
                                             borovskoe=borovskoe,
                                             vtoroe_uspenskoe=vtoroe_uspenskoe))
    )
    return markup


# # Создаем функцию, которая отдает клавиатуру с доступными товарами, исходя из выбранной категории и подкатегории
# async def items_keyboard(category, subcategory):
#     CURRENT_LEVEL = 2
#
#     # Устанавливаю row_width = 1, чтобы показывалась одна кнопка в строке на товар
#     markup = InlineKeyboardMarkup(row_width=1)
#
#     # Забираем список товаров из базы данных с выбранной категорией и подкатегорией, и проходим по нему
#     items = await get_items(category, subcategory)
#     for item in items:
#         # Сформируем текст, который будет на кнопке
#         button_text = f"{item.name} - ${item.price}"
#
#         # Сформируем колбек дату, которая будет на кнопке
#         callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
#                                            category=category, subcategory=subcategory,
#                                            item_id=item.id)
#         markup.insert(
#             InlineKeyboardButton(
#                 text=button_text, callback_data=callback_data)
#         )
#
#     # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
#     # пользователя на уровень назад - на уровень 1 - на выбор подкатегории
#     markup.row(
#         InlineKeyboardButton(
#             text="Назад",
#             callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
#                                              category=category))
#     )
#     return markup


# Создаем функцию, которая отдает клавиатуру с кнопками "купить" и "назад" для выбранного товара
def item_keyboard(category, subcategory, item_id):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text=f"Купить",
            callback_data=buy_item.new(item_id=item_id)
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             category=category, subcategory=subcategory))
    )
    return markup
