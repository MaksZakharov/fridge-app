"""
Модуль утилит для обработки текстовых заметок о продуктах.
"""

import datetime
from decimal import Decimal


def parse_note(note):
    """
    Преобразует текстовую заметку в название продукта, количество и срок.

    :param note: Строка вида "<название> <кол-во> [<срок годности>]".
    :return: Кортеж (title, amount, expiration_date)
    """
    parts = note.split()
    if len(parts) < 2:
        raise ValueError("Формат: '<название> <кол-во> [<дата>]'.")

    try:
        # Пытаемся распарсить дату в формате 'YYYY-MM-DD'
        datetime.datetime.strptime(parts[-1], "%Y-%m-%d")
        expiration_date = parts[-1]
        amount = Decimal(parts[-2])
        title = ' '.join(parts[:-2])
    except ValueError:
        # Если не получилось, считаем, что даты нет
        expiration_date = None
        amount = Decimal(parts[-1])
        title = ' '.join(parts[:-1])

    return title, amount, expiration_date
