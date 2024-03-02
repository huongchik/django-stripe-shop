from django.db import models
from .validators import validate_min_price, get_exchange_rate
from decimal import Decimal, ROUND_HALF_UP


class Item(models.Model):
    """
    Определяет товар, доступный для покупки. Включает в себя название, описание, цену и валюту.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")

    def clean(self):
        """
        Вызывается для валидации данных модели перед сохранением. Проверяет минимальную цену товара.
        """
        validate_min_price(self.price, self.currency)


class Order(models.Model):
    """
    Определяет заказ, который может содержать множество товаров, а также связанные скидки и налоги.
    """
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(
        "Discount", on_delete=models.SET_NULL, null=True, blank=True
    )
    tax = models.ForeignKey("Tax", on_delete=models.SET_NULL, null=True, blank=True)

    def get_total_cost(self, to_currency="EUR"):
        """
        Рассчитывает общую стоимость заказа, конвертируя цены товаров в указанную валюту и применяя скидки и налоги.
        """
        total_cost = Decimal("0.0")
        for item in self.items.all():
            if item.currency != to_currency:
                exchange_rate = get_exchange_rate(item.currency, to_currency)
                item_cost_in_eur = item.price * exchange_rate
            else:
                item_cost_in_eur = item.price
            total_cost += item_cost_in_eur

        if self.discount:
            total_cost *= (Decimal("100.0") - self.discount.discount_percent) / Decimal(
                "100.0"
            )
        if self.tax:
            total_cost *= (Decimal("100.0") + self.tax.tax_percent) / Decimal("100.0")

        total_cost = total_cost.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return total_cost


class Discount(models.Model):
    """
    Определяет скидку, которая может быть применена к заказу. Включает в себя название и процент скидки.
    """
    name = models.CharField(max_length=100)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.discount_percent}%"


class Tax(models.Model):
    """
    Определяет налог, который может быть применен к заказу. Включает в себя название и процент налога.
    """
    name = models.CharField(max_length=100)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.tax_percent}%"
