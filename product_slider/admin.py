from django.contrib import admin
from .models import Slider,Banner


@admin.register(Slider)
class AdminSlider(admin.ModelAdmin):
    list_display = ['title','order']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title' , 'image']
    
