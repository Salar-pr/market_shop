from django.db import models
from product.models import Product
from django.conf import settings


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "pending", "در حال انتظار"
        PAID = "paid", "پرداخت شده"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    status = models.CharField(
        max_length=155,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    payment_date = models.DateTimeField(
        verbose_name='تاریخ پرداخت',
        null=True,
        blank=True
    )
    ref_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='کد پیگیری'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.owner.username}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    
    def clear_items(self):
        self.items.all().delete()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
    )
    item = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
    )
    count = models.PositiveIntegerField(
        verbose_name='تعداد',
    )

    def get_total_price(self):
        return self.price * self.count

    def save(self, *args, **kwargs):
        self.price = str(self.price).replace(',', '')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.title} x {self.count} for Order {self.order.owner}"

    

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    first_name = models.CharField(max_length=100, verbose_name="نام")
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی")
    email = models.EmailField(verbose_name="آدرس ایمیل")
    phone_number = models.CharField(max_length=15, verbose_name="شماره تلفن")
    address = models.CharField(max_length=255, null=True,blank=True,verbose_name="آدرس محل تحویل")
    city = models.CharField(max_length=100, verbose_name="شهر")
    postcode = models.CharField(max_length=20, verbose_name="کد پستی")
    card_number = models.CharField(max_length=16, verbose_name="شماره کارت")

    def __str__(self):
        return f"{self.user.username} - {self.first_name} {self.last_name}"

  
