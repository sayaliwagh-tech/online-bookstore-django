

from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("success/", views.order_success, name="order_success"),
    path("orders/", views.my_orders, name="my_orders"),
    path(
        "payment-success/",
        views.payment_success,
        name="payment_success"
    ),
    path(
        "invoice/<int:order_id>/",
        views.download_invoice,
        name="download_invoice"
    ),
    path(
        "cancel/<int:id>/",
        views.cancel_order, 
        name="cancel_order"
    ),
    path(
        "buy-again/<int:id>/",
        views.buy_again,
        name="buy_again"
    ),
]