"""
Модуль с юнит-тестами для функций core из приложения 'Холодильник'.
"""

import datetime
from decimal import Decimal

from fridge.core import add, add_by_note, get_amount, get_expired


def test_add_and_get_amount():
    """
    Проверяет добавление нескольких партий одного продукта и
    корректность подсчёта общего количества.
    """
    goods = {}
    add(goods, 'Яйца', Decimal('4'), '2023-12-01')
    add(goods, 'Яйца', Decimal('3'), '2023-12-05')
    assert get_amount(goods, 'яйца') == Decimal('7')


def test_add_by_note():
    """
    Проверяет добавление продукта из текстовой заметки.
    """
    goods = {}
    add_by_note(goods, 'Морковь 2.5 2023-12-10')
    assert goods['Морковь'][0]['amount'] == Decimal('2.5')


def test_get_expired():
    """
    Проверяет определение просроченных продуктов.
    """
    goods = {
        'Хлеб': [{
            'amount': Decimal('1'),
            'expiration_date': datetime.date.today()
        }],
        'Вода': [{
            'amount': Decimal('2'),
            'expiration_date': None
        }]
    }
    result = get_expired(goods)
    assert result == [('Хлеб', Decimal('1'))]


def test_find():
    """
    Проверяет поиск продуктов по подстроке без учёта регистра.
    """
    goods = {
        'Яйца': [{'amount': Decimal('1'), 'expiration_date': None}],
        'Яйца гусиные': [{'amount': Decimal('4'), 'expiration_date': None}],
        'Морковь': [{'amount': Decimal('2'), 'expiration_date': None}]
    }
    from fridge.core import find
    result = find(goods, 'яйц')
    assert sorted(result) == ['Яйца', 'Яйца гусиные']


def test_get_expired_with_advance():
    """
    Проверяет, что get_expired учитывает in_advance_days.
    """
    today = datetime.date.today()
    goods = {
        'Молоко': [{
            'amount': Decimal('1'),
            'expiration_date': today + datetime.timedelta(days=2)
        }],
        'Хлеб': [{
            'amount': Decimal('1'),
            'expiration_date': today + datetime.timedelta(days=5)
        }]
    }

    # За 1 день — ничего
    assert get_expired(goods, 1) == []

    # За 2 дня — только Молоко
    assert get_expired(goods, 2) == [('Молоко', Decimal('1'))]

    # За 5 дней — оба продукта
    result = get_expired(goods, 5)
    expected = [('Молоко', Decimal('1')), ('Хлеб', Decimal('1'))]
    assert sorted(result) == sorted(expected)
