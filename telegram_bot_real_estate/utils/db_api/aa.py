import json  # Подключили библиотеку

with open('C:/Users/Kirya/Downloads/jsss.json', 'r', encoding='utf-8') as f:  # открыли файл
    text = json.load(f)  # загнали все из файла в переменную
    #print(text)  # вывели результат на экран

# for txt in text:  # создали цикл, который будет работать построчно
#     print(txt)
pred = text[0]

print(pred)
# a = [1, 2, 3]
# b = [1, 5, 3]
# print(list(set(a+b)))

# def kyky(a='0', b='0', *args):

# def kaka(a, b=4, c=4):
#     print(a+b+c)
# in_kaka = 'a=3'
# kaka(f'in_kaka')

# dom = False
# uchastok = False
# slovarik = {'dom':dom, 'uchastok':uchastok}
# estate_type = 'uchastok'
# try:
#     slovarik[estate_type] = not slovarik[estate_type]
# except KeyError:
#     pass
# # for x in slovarik.keys():
# #     if x == estate_type:
# #
# #         bool = eval(f'not {estate_type}')
# # print(dom, uchastok)
# print(slovarik.values())

# estate_type = 'nedom'
# dom = True
# nedom = False
# check = eval(estate_type)
# # print(check)
# condition = ['a']
# if condition:
#     print('aga')
# a = 'a'
# print(not bool(not a))
# def fucc(a, b, **kwargs):
#     print(a, b)
# fucc(1, 2, c=3)