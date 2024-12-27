from django.db import models
from django.urls import reverse
from uuid import uuid4
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils.html import format_html
from django.contrib.humanize.templatetags.humanize import naturalday
from PIL import Image
from django.utils.text import format_lazy,slugify
from account.models import User






class Color(models.Model):
    title = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'color'
        verbose_name_plural = 'رنگ ها'
        
    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.SET_NULL,
        verbose_name="سر دسته",
        )
    title = models.CharField(max_length=255,verbose_name="عنوان",unique=True)
    slug = models.SlugField(max_length=255,unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

        
    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ['created_at']
        
    def __str__(self) -> str:
        return self.title
    
    def humanuze_date(self):
        return naturalday(self.created_at)
    
    
    def get_child_products(self):
        childs = self.children.all()
        child_products = Product.objects.filter(category__in=childs)
        own_products = Product.objects.filter(category=self)
        all_products = child_products | own_products
        return all_products.distinct()


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class ProductSpecification(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    attribute = models.CharField(max_length=255)
        
    def __str__(self) -> str:
        return self.attribute
    

class Product(models.Model):
    title = models.CharField(max_length=255,unique=True)
    category = models.ForeignKey(Category,null=True,blank=True,on_delete=models.PROTECT,related_name="products")
    uuid = models.UUIDField(default=uuid4,unique=True)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=12,decimal_places=0)
    number = models.PositiveIntegerField(default=0)
    colors = models.ManyToManyField(Color)
    image = models.ImageField(upload_to="products" ,width_field=100,height_field=150)
    count_sold = models.PositiveIntegerField(default=0)
    is_special = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    update_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    discount = models.PositiveIntegerField(
        default=0,
        validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
        ]
    )
    
    
    class Meta:
        verbose_name = "product"
        verbose_name_plural = "محصول ها"
        
    def __str__(self) -> str:
        return self.title
    
    def thumbnail(self):
        image_tag = f"<img src='{self.image.url}' alt='{self.title}' width='10' height='10' >"
        return format_html(image_tag)
    thumbnail.short_description = "عکس"
    
    def Price(self):
        return format_lazy("{:,}",self.price)
    
    def get_total_price(self):
        discount_price = self.price * self.discount / 100
        format_price=self.price - discount_price
        return format_lazy("{:,}", format_price)
    
    def get_absulote_url(self):
        return reverse("product:product_detail",args=[self.uuid])
    
    def status(self):
        if self.number > 0:
            return True
        return False
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # تغییر اندازه تصویر
        img = Image.open(self.image.path)

        # تنظیم سایز تصویر
        max_size = (300, 300)  # سایز دلخواه (عرض، ارتفاع)
        img.thumbnail(max_size)

        # ذخیره تصویر تغییر اندازه داده‌شده
        img.save(self.image.path)
    
    
    
class Gallery(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="galleries")
    title = models.CharField(max_length=255,unique=True)
    image = models.ImageField(upload_to="galleries",width_field=100,height_field=150)
    
    
    class Meta:
        verbose_name = "gallery"
        verbose_name_plural = "گالری"
        
    def __str__(self) -> str:
        return self.title
    
    
    
class ProductSpecificationValue(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="specifications")
    specification = models.ForeignKey(ProductSpecification,on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.value
    


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()  
    point = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)],blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True) 



    


