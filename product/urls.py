from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path("", views.home, name="home"),
    path("category/<slug:slug>", views.category, name="category"),
    path("category/", views.category_all, name="category_all"),
    path("<uuid:uuid>", views.product_detail, name="product_detail"),
    
]
