import os
import django
from decimal import Decimal

# Установите настройки Django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "myproject.settings"
)  # замените 'myproject' на имя вашего проекта
django.setup()

from myapp.models import Item, Order, Discount, Tax


def seed_data():
    # Создание тестовых данных для модели Item
    items = [
        {
            "name": "Laptop",
            "description": "High-end gaming laptop",
            "price": Decimal("1500.00"),
            "currency": "USD",
        },
        {
            "name": "Smartphone",
            "description": "Latest model smartphone",
            "price": Decimal("999.99"),
            "currency": "USD",
        },
        {
            "name": "Headphones",
            "description": "Noise-cancelling headphones",
            "price": Decimal("199.99"),
            "currency": "EUR",
        },
        {
            "name": "Coffee Machine",
            "description": "Automatic coffee machine",
            "price": Decimal("250.00"),
            "currency": "USD",
        },
    ]

    for item_data in items:
        item, created = Item.objects.get_or_create(**item_data)
        if created:
            print(f"Создан товар: {item.name}")
        else:
            print(f"Товар уже существует: {item.name}")

    # Создание тестовых данных для модели Discount
    discounts = [
        {"name": "Holiday Discount", "discount_percent": Decimal("10.00")},
        {"name": "Clearance Discount", "discount_percent": Decimal("20.00")},
    ]

    for discount_data in discounts:
        discount, created = Discount.objects.get_or_create(**discount_data)
        if created:
            print(f"Создана скидка: {discount.name}")
        else:
            print(f"Скидка уже существует: {discount.name}")

    # Создание тестовых данных для модели Tax
    taxes = [
        {"name": "VAT", "tax_percent": Decimal("20.00")},
        {"name": "Sales Tax", "tax_percent": Decimal("5.00")},
    ]

    for tax_data in taxes:
        tax, created = Tax.objects.get_or_create(**tax_data)
        if created:
            print(f"Создан налог: {tax.name}")
        else:
            print(f"Налог уже существует: {tax.name}")

    # Создание тестовых данных для модели Order
    orders = [
        {"items": [1, 2], "discount": 1, "tax": 1},
        {"items": [3, 4], "discount": 2, "tax": 2},
    ]

    for order_data in orders:
        order = Order()
        order.save()  # Сохраняем заказ перед добавлением ManyToMany поля
        order.items.set(order_data["items"])
        order.discount_id = order_data["discount"]
        order.tax_id = order_data["tax"]
        order.save()
        print(f"Создан заказ с ID: {order.id}")


if __name__ == "__main__":
    seed_data()
