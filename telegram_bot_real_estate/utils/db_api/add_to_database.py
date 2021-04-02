from utils.db_api.db_commands import add_item

import json

import asyncio

from utils.db_api.database import create_db


# Используем эту функцию, чтобы заполнить базу данных товарами
async def add_estates():
    with open('C:/Users/Kirya/Downloads/jsss.json', 'r', encoding='utf-8') as f:  # открыли файл
        text = json.load(f)  # загнали все из файла в переменную
        for estate in text:
            await add_item(deal_type=estate['deal_type'], estate_type=estate['estate_type'], estate_direction=estate['estate_direction'], otdelka=estate['otdelka'],
                           how_far=estate['how_far'], ploshad_doma=estate['ploshad_doma'], ploshad_uchastka=estate['ploshad_uchastka'], floors=estate['floors'],
                           spalni=estate['spalni'], show_first=estate['show_first'], )


# async def add_items():
#     await add_item(name="ASUS",
#                    category_name="🔌 Электроника", category_code="Electronics",
#                    subcategory_name="🖥 Компьютеры", subcategory_code="PCs",
#                    price=100, photo="-")
#     await add_item(name="DELL",
#                    category_name="🔌 Электроника", category_code="Electronics",
#                    subcategory_name="🖥 Компьютеры", subcategory_code="PCs",
#                    price=100, photo="-")
#     await add_item(name="Apple",
#                    category_name="🔌 Электроника", category_code="Electronics",
#                    subcategory_name="🖥 Компьютеры", subcategory_code="PCs",
#                    price=100, photo="-")
#     await add_item(name="Iphone",
#                    category_name="🔌 Электроника", category_code="Electronics",
#                    subcategory_name="☎️ Телефоны", subcategory_code="Phones",
#                    price=100, photo="-")
#     await add_item(name="Xiaomi",
#                    category_name="🔌 Электроника", category_code="Electronics",
#                    subcategory_name="☎️ Телефоны", subcategory_code="Phones",
#                    price=100, photo="-")
#     await add_item(name="PewDiePie",
#                    category_name="🛍 Услуги Рекламы", category_code="Ads",
#                    subcategory_name="📹 На Youtube", subcategory_code="Youtube",
#                    price=100, photo="-")
#     await add_item(name="Топлес",
#                    category_name="🛍 Услуги Рекламы", category_code="Ads",
#                    subcategory_name="📹 На Youtube", subcategory_code="Youtube",
#                    price=100, photo="-")
#     await add_item(name="Орлёнок",
#                    category_name="🛍 Услуги Рекламы", category_code="Ads",
#                    subcategory_name="🗣 На Вконтакте", subcategory_code="VK",
#                    price=100, photo="-")
#     await add_item(name="МДК",
#                    category_name="🛍 Услуги Рекламы", category_code="Ads",
#                    subcategory_name="🗣 На Вконтакте", subcategory_code="VK",
#                    price=100, photo="-")


loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
loop.run_until_complete(add_estates())
