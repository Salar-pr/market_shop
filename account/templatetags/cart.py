from django import template
from product_order.models import Order,OrderItem

register = template.Library()


@register.inclusion_tag("product_order/templatetags/cart.html", takes_context=True)
def get_cart_items(context):
    request = context["request"]
    order,created = Order.objects.get_or_create(
            owner = request.user,
            status=Order.OrderStatus.PENDING,)
    
    items = order.items.all()
    context = {  
        "order":order,
        "items":items,
        "total_price": order.get_total_price() if order else 0,
    }
    
    return context
    
    