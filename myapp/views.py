from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Item, Order
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Установите ключ API Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def item_page(request, id):
    """
    Отображает страницу товара с кнопкой для покупки.
    """
    item = get_object_or_404(Item, id=id)
    context = {
        'item': item,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'item.html', context)
def order_page(request, id):
    """
    Отображает страницу заказа с деталями заказа.
    """
    order = get_object_or_404(Order, id=id)
    
    total_cost = order.get_total_cost()
    
    context = {
        'order': order,
        'total_cost': total_cost,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY  # Ensure you have this in your settings
    }
    
    return render(request, 'order.html', context)

def payment_success(request):
    """
    Отображает страницу об успешной покупке.
    """
    return render(request, 'payment_success.html', {})


@csrf_exempt
@require_http_methods(["POST"])
def create_payment_intent(request, id):
    """
    Создает намерение платежа (PaymentIntent) для конкретного товара с использованием Stripe.
    """
    item = get_object_or_404(Item, id=id)
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(item.price * 100),
            currency=item.currency,
            payment_method_types=['card'],
            description=f'Оплата за {item.name}'
        )
        return JsonResponse({'clientSecret': payment_intent.client_secret})
    except Exception as e:
        print(f"Ошибка при создании PaymentIntent: {str(e)}")  # Для отладки
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def create_payment_intent_for_order(request, order_id):
    """
    Создает намерение платежа (PaymentIntent) для заказа, включая общую стоимость, с учетом скидок и налогов.
    """
    order = get_object_or_404(Order, id=order_id)
    currency = order.items.first().currency 

    total_cost = order.get_total_cost() 

    metadata = {
        'order_id': order_id,
        'discount': order.discount.name if order.discount else "No discount",
        'tax': order.tax.name if order.tax else "No tax"
    }

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(total_cost * 100), 
            currency=currency,
            payment_method_types=['card'],
            description=f'Payment for Order #{order_id}',
            metadata=metadata 
        )
        return JsonResponse({'clientSecret': payment_intent.client_secret})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
