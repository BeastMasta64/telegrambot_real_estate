from sqlalchemy import (Column, Integer, String, Sequence)
from sqlalchemy import sql
from utils.db_api.database import db


# Создаем класс таблицы товаров
class Estate(db.Model):
    __tablename__ = 'estates'
    query: sql.Select

    # Уникальный идентификатор дома
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    deal_type = Column(String(40))
    estate_type = Column(String(50))
    estate_direction = Column(String(50))
    otdelka = Column(String(50))
    how_far = Column(Integer)
    ploshad_doma = Column(String(50))
    ploshad_uchastka = Column(String(50))
    floors = Column(String(50))
    spalni = Column(Integer)
    show_first = Column(Integer)

# class Item(db.Model):
# __tablename__ = 'items'
# query: sql.Select
#
# # Уникальный идентификатор товара
# id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
#
# # Код категории (для отображения в колбек дате)
# category_code = Column(String(20))
#
# # Название категории (для отображения в кнопке)
# category_name = Column(String(50))
#
# # Код подкатегории (для отображения в колбек дате)
# subcategory_code = Column(String(50))
#
# # Название подкатегории (для отображения в кнопке)
# subcategory_name = Column(String(20))
#
# # Название, фото и цена товара
# name = Column(String(50))
# photo = Column(String(250))
# price = Column(Integer)

    def __repr__(self):
        return f"""
Недвижимость № {self.id} - "{self.deal_type}"
{self.estate_type} {self.estate_direction} {self.otdelka} {self.how_far} {self.ploshad_doma} {self.ploshad_uchastka} {self.floors} {self.spalni} {self.show_first}"""
