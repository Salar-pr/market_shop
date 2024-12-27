from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddItem, UserProfileForm
from .models import Order, OrderItem, UserProfile
from product.models import Product
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import transaction


def add_order_item(request):
    if request.method == "POST":
        form = AddItem(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            count = cd["count"]
            
            if count < 0:
                count = 1

            try:
                with transaction.atomic():
                    order = Order.objects.get(owner=request.user, status=Order.OrderStatus.PENDING)
                    product = get_object_or_404(Product, id=cd["product_id"])
                    
                    item = OrderItem(
                        order=order,
                        item=product,
                        price=product.get_total_price(),
                        count=count
                    )
                    item.save()
                    
                    return redirect("product:product_detail", uuid=product.uuid)
            except Order.DoesNotExist:
                return redirect("product:home", error="No pending order found.")
            except Exception as e:
                return redirect("product:home", error=str(e))

    return redirect("product:home")


@login_required
def buy_order(request):
    pending_order = Order.objects.filter(
        owner=request.user,
        status=Order.OrderStatus.PENDING
    ).first()

    if not pending_order:
        messages.error(request, "سبد خرید شما خالی است.")
        return redirect("product:home")

    items = pending_order.items.all()
    total_price = sum(item.get_total_price() for item in items)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            
            pending_order.status = Order.OrderStatus.PAID
            pending_order.payment_date = timezone.now()
            pending_order.save()
            pending_order.items.all().delete()
            messages.success(request, "پرداخت با موفقیت انجام شد!")
            return redirect("product:home")
            
        else:
            
            messages.warning(request, "اطلاعات فرم صحیح نیست. لطفاً دوباره تلاش کنید.")

    else:
        form = UserProfileForm(instance=request.user)

    context = {
        "items": items,
        "total_price": total_price,
        "form": form,
    }

    return render(request, 'product/checkout.html', context)
