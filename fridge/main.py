"""
Точка входа в приложение 'Холодильник'.
Позволяет добавить продукты, выполнить поиск, получить количество
и список просроченных продуктов.
"""

from decimal import Decimal

from fridge.core import add, add_by_note, find, get_amount, get_expired


def main():
    """Основной скрипт запуска приложения 'Холодильник'."""
    goods = {}

    # Добавление продуктов
    add(goods, 'Яйца', Decimal('10'), '2023-12-10')
    add_by_note(goods, 'Морковь 2 2023-12-05')
    add_by_note(goods, 'Вода 1.5')

    # Поиск по ключевому слову
    print("Поиск 'яйца':", find(goods, 'яйца'))

    # Получение общего количества по ключу
    print("Сколько воды:", get_amount(goods, 'вода'))

    # Получение просроченных продуктов на ближайшие 5 дней
    expired = get_expired(goods, 5)
    print("Просроченные:")
    for name, amount in expired:
        print(f"- {name}: {amount} кг")

    # Вывод всех продуктов в холодильнике
    print("\nСодержимое холодильника:")
    for product, batches in goods.items():
        print(f"{product}:")
        for batch in batches:
            amount = batch['amount']
            exp = batch['expiration_date']
            print(f"  - {amount} кг, срок: {exp}")
