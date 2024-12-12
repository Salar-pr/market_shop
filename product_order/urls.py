from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("add-item/", views.add_order_item, name="add_order_item"),
    path("buy-item/", views.buy_order, name="buy_order"),
]
