from typing import List
from sqlalchemy import and_, or_

from utils.db_api.models import Estate
from utils.db_api.database import db


# Функция для создания новой недвижимости в базе данных. Принимает все возможные аргументы, прописанные в Estate
async def add_estate(**kwargs):
    new_estate = await Estate(**kwargs).create()
    return new_estate


# Функция для вывода типов сделок
async def get_deal_type() -> List[Estate]:
    return await Estate.query.distinct(Estate.deal_type).gino.all()


# Функция для вывода типов недвижимости с учетом выбранного типа сделки
async def get_estate_type(deal_type) -> List[Estate]:
    return await Estate.query.distinct(Estate.estate_type).where(Estate.deal_type == deal_type).gino.all()


# Функция для вывода направлений недвижимости с учетом выбранных условий
async def get_estate_direction(deal_type, dom, uchastok, townhouse, apartamenti, kvartira) -> List[Estate]:
    # Прописываем условия для вывода (выбранный тип сделки и выбранные типы недвижимости)
    condition1 = [Estate.deal_type == deal_type]
    conditions_estate_types = []
    # Если передали типы недвижимостей, то добавляем их в условие
    if dom:
        conditions_estate_types.append(Estate.estate_type == 'dom')
    if uchastok:
        conditions_estate_types.append(Estate.estate_type == 'uchastok')
    if townhouse:
        conditions_estate_types.append(Estate.estate_type == 'townhouse')
    if apartamenti:
        conditions_estate_types.append(Estate.estate_type == 'apartamenti')
    if kvartira:
        conditions_estate_types.append(Estate.estate_type == 'kvartira')

    # Возвращаем список недвижимости, подходящий под выбранные условия
    return await Estate.query.distinct(Estate.estate_direction).where(
        and_((or_(*conditions_estate_types)), condition1)).gino.all()


# Функция для вывода типов отделок недвижимости с учетом выбранных условий
async def get_estate_otdelka(deal_type, dom, uchastok, townhouse, apartamenti, kvartira, novorijskoe, rublevskoe,
                                 kievskoe, dmitrovskoe, rublevo_uspenskoe, minskoe, ilinskoe, kalujskoe, borovskoe,
                                 vtoroe_uspenskoe) -> List[Estate]:
    # Прописываем условия для вывода (выбранный тип сделки, выбранные типы недвижимости, выбранные направления)
    condition1 = [Estate.deal_type == deal_type]
    conditions_estate_types = []
    # Если передали типы недвижимостей, то добавляем их в условие
    if dom:
        conditions_estate_types.append(Estate.estate_type == 'dom')
    if uchastok:
        conditions_estate_types.append(Estate.estate_type == 'uchastok')
    if townhouse:
        conditions_estate_types.append(Estate.estate_type == 'townhouse')
    if apartamenti:
        conditions_estate_types.append(Estate.estate_type == 'apartamenti')
    if kvartira:
        conditions_estate_types.append(Estate.estate_type == 'kvartira')

    conditions_estate_directions = []
    # Если передали направления, то добавляем их в условие
    if novorijskoe:
        conditions_estate_directions.append(Estate.estate_type == 'novorijskoe')
    if rublevskoe:
        conditions_estate_directions.append(Estate.estate_type == 'rublevskoe')
    if kievskoe:
        conditions_estate_directions.append(Estate.estate_type == 'kievskoe')
    if dmitrovskoe:
        conditions_estate_directions.append(Estate.estate_type == 'dmitrovskoe')
    if rublevo_uspenskoe:
        conditions_estate_directions.append(Estate.estate_type == 'rublevo_uspenskoe')
    if minskoe:
        conditions_estate_directions.append(Estate.estate_type == 'minskoe')
    if ilinskoe:
        conditions_estate_directions.append(Estate.estate_type == 'ilinskoe')
    if kalujskoe:
        conditions_estate_directions.append(Estate.estate_type == 'kalujskoe')
    if borovskoe:
        conditions_estate_directions.append(Estate.estate_type == 'borovskoe')
    if vtoroe_uspenskoe:
        conditions_estate_directions.append(Estate.estate_type == 'vtoroe_uspenskoe')
    # Возвращаем список недвижимости, подходящий под выбранные условия
    return await Estate.query.distinct(Estate.otdelka_front).where(
        and_((or_(*conditions_estate_types)), condition1, (or_(*conditions_estate_directions)))).gino.all()


# Функция для подсчета недвижимости с выбранными условиями
async def count_estates(deal_type, estate_type=None, dom=None, uchastok=None, townhouse=None, apartamenti=None,
                        kvartira=None):
    # Прописываем условия для вывода (выбранный тип сделки и выбранные типы недвижимости)
    conditions = [Estate.deal_type == deal_type]
    conditions_estate_types = []

    # Если передали типы недвижимостей, то добавляем их в условие
    if dom:
        conditions.append(Estate.estate_type == 'dom')
    if uchastok:
        conditions.append(Estate.estate_type == 'uchastok')
    if townhouse:
        conditions.append(Estate.estate_type == 'townhouse')
    if apartamenti:
        conditions.append(Estate.estate_type == 'apartamenti')
    if kvartira:
        conditions.append(Estate.estate_type == 'kvartira')

    # Функция подсчета товаров с указанными условиями
    total = await db.select([db.func.count()]).where(or_(*conditions)).gino.scalar()
    return total


#######################################################################################################
# Функция вывода всех товаров, которые есть в переданных категории и подкатегории
async def get_items(category_code, subcategory_code) -> List[Estate]:
    item = await Estate.query.where(
        and_(Estate.category_code == category_code,
             Estate.subcategory_code == subcategory_code)
    ).gino.all()
    return item


# Функция для получения объекта товара по его айди
async def get_item(item_id) -> Estate:
    item = await Estate.query.where(Estate.id == item_id).gino.first()
    return item
