from django import template
from ..models import Category

register = template.Library()

@register.inclusion_tag('product/templatetags/menu.html')
def get_categories():
    categories = Category.objects.filter(parent__isnull=True)
    return {
        "categories":categories,  
    }


@register.inclusion_tag('product/includes/navbar.html',takes_context=True)
def navbar(context):
    request = context["request"]
    categories = Category.objects.filter(parent__isnull=True)[:3]
    return {
        "categories":categories,  
    }

    