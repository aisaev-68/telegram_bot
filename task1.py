import re
def check_city(mess):
    """
        Функция проверки на корректность ввода названия города.
    """
    if len(re.findall(r'\b[a-zA-Z]{0,10},[a-zA-Z]{0,10}', mess)) > 1:
        print(mess)
    else:
        print('Error')

print(len(re.findall(r'^[^\W\d_]+\.?(?:[-\s][^\W\d_]+\.?)*$', 'Москва1')))


