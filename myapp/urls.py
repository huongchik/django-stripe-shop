from django.urls import path
from .views import item_page, create_payment_intent, create_payment_intent_for_order, order_page, payment_success

urlpatterns = [
    path('item/<int:id>/', item_page, name='item-page'),
    path('order/<int:id>/', order_page, name='order-page'),
    path('create-payment-intent/<int:id>/', create_payment_intent, name='create-payment-intent'),
    path('create-payment-intent/order/<int:order_id>/', create_payment_intent_for_order, name='create-payment-intent-for-order'),
    path('payment-success/', payment_success, name='payment-success'),
]
