"""
Основной модуль логики приложения 'Холодильник'.
Содержит функции для добавления, поиска и анализа продуктов.
"""

import datetime
from decimal import Decimal

from fridge.utils import parse_note


def add(items, title, amount, expiration_date=None):
    """
    Добавляет партию продукта в словарь товаров.

    :param items: Словарь с продуктами.
    :param title: Название продукта.
    :param amount: Количество продукта (Decimal).
    :param expiration_date: Срок годности в формате 'YYYY-MM-DD' или None.
    """
    if expiration_date:
        expiration_date = datetime.datetime.strptime(
            expiration_date, '%Y-%m-%d'
        ).date()
    batch = {'amount': amount, 'expiration_date': expiration_date}
    items.setdefault(title, []).append(batch)


def add_by_note(items, note):
    """
    Добавляет продукт по текстовой заметке.

    :param items: Словарь с продуктами.
    :param note: Строка вида "<название> <кол-во> [<срок годности>]".
    """
    title, amount, expiration_date = parse_note(note)
    add(items, title, amount, expiration_date)


def find(items, needle):
    """
    Ищет продукты по подстроке в названии (без учёта регистра).

    :param items: Словарь с продуктами.
    :param needle: Строка для поиска.
    :return: Список найденных названий.
    """
    needle = needle.lower()
    return [title for title in items if needle in title.lower()]


def get_amount(items, needle):
    """
    Возвращает общее количество продукта по ключевому слову.

    :param items: Словарь с продуктами.
    :param needle: Строка для поиска.
    :return: Общее количество найденных продуктов (Decimal).
    """
    total = Decimal('0')
    for title in find(items, needle):
        for batch in items[title]:
            total += batch['amount']
    return total


def get_expired(items, in_advance_days=0):
    """
    Возвращает список просроченных продуктов и их количества.

    :param items: Словарь с продуктами.
    :param in_advance_days: Кол-во дней до срока годности (по умолчанию 0).
    :return: Список кортежей (название, общее количество).
    """
    expired = []
    today = datetime.date.today()
    for title, batches in items.items():
        total = Decimal('0')
        for batch in batches:
            exp = batch['expiration_date']
            deadline = today + datetime.timedelta(days=in_advance_days)
            if exp and exp <= deadline:
                total += batch['amount']
        if total > 0:
            expired.append((title, total))
    return expired
