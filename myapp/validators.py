from django.core.exceptions import ValidationError
from decimal import Decimal
import requests
from bs4 import BeautifulSoup

def get_exchange_rate(from_currency, to_currency='EUR'):
    """
    Получает текущий обменный курс между двумя валютами с использованием Google Поиска.
    """
    # Формируем запрос для Google Поиска
    query = f"{from_currency} to {to_currency} exchange rate"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Ищем элемент с курсом валюты
        rate = soup.find('div', class_='BNeawe iBp4i AP7Wnd')
        if rate:
            rate_text = rate.text.replace(',', '.')
            try:
                return Decimal(rate_text.split(' ')[0])
            except ValueError:
                print("Не удалось преобразовать курс в число.")
                return None
    else:
        print("Ошибка при выполнении запроса к Google.")
        return None


def validate_min_price(value, currency):
    """
    Проверяет, что значение цены товара после конвертации в EUR не меньше минимальной суммы.
    """
    value = Decimal(value)
    if currency != 'EUR':
        rate = get_exchange_rate(currency)
        value_in_eur = value * Decimal(rate)
    else:
        value_in_eur = value
        

    # Проверка минимальной суммы после конвертации в евро
    if value_in_eur < Decimal('0.5'):
        raise ValidationError(f'Сумма после конвертации в евро должна быть не менее 0.5 евро. Вы ввели: {value_in_eur}')


