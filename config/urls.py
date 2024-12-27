
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from account.views import signup, CustomLoginView


urlpatterns = [
    path("", include('product.urls')),
    path("", include('about_us.urls')),
    path('admin/', admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    path("order/", include("product_order.urls")),


    path('login/', CustomLoginView.as_view(), name='login'),
    path('singup/', signup, name='signup'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
