from django.shortcuts import render
from product.models import Product
from .models import AboutUs


def about_us(request):
    about_us = AboutUs.objects.all()
    product_count_sold = Product.objects.filter(count_sold__gte=36).order_by('-count_sold')[:5]
    product_created_at = Product.objects.order_by('-created_at')[:5]
    special_products = Product.objects.filter(
        is_special=True).order_by('-discount')
    
    context = {
        'special_products':special_products,
        'product_count_sold':product_count_sold,
        'product_created_at':product_created_at,
        'about_us':about_us,

    }

    return render(request, 'product/about-us.html', context)
