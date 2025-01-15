from django.shortcuts import render, get_object_or_404, redirect
from product.models import Product, Category, Comment
from product.forms import CommentForm
from product_slider.models import Slider,Banner
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.db.models import Avg


def home(request):
    categories = Category.objects.all()
    products = Product.objects.none()
    for category in categories:
        # محصولات مرتبط با دسته‌بندی و فرزندانش
        products = Product.objects.filter(
            category__in=category.children.all()) | Product.objects.filter(category=category)
    sliders = Slider.objects.all()
    special_products = Product.objects.filter(
        is_special=True).order_by('-discount')
    parent_category = Category.objects.filter(parent__isnull=True)[:2]
    Banners = Banner.objects.all()
    products_all =  Product.objects.annotate(
        avg_rating=Avg('comments__point'))
    product_count_sold = products_all.filter(count_sold__gte=36).order_by('-count_sold')[:5]
    product_created_at = products_all.order_by('-created_at')[:5]

    

    context = {
        "sliders": sliders,
        "special_products": special_products,
        "parent_category": parent_category,
        "Banners": Banners,
        'products': products,  
        'products_all':products_all,
        'product_count_sold':product_count_sold,
        'product_created_at':product_created_at,
    }
    return render(request, "product/index.html", context=context)


def product_detail(request, uuid):
    
    product = get_object_or_404(Product, uuid=uuid)
    comments = Comment.objects.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user  # کاربر لاگین‌شده
            comment.save()
            messages.success(request, "نظر شما با موفقیت ثبت شد.")
            return redirect('product:product_detail', uuid=product.uuid)
    else:
        form = CommentForm()
    product_count_sold = Product.objects.filter(count_sold__gte=36).order_by('-count_sold')[:5]
    product_created_at = Product.objects.order_by('-created_at')[:5]
    special_products = Product.objects.filter(
        is_special=True).order_by('-discount')

    

    context = {
        "product": product,
        "comments": comments,
        "form": form,
        'product_count_sold':product_count_sold,
        'product_created_at':product_created_at,
        "special_products": special_products,
    }

    return render(request, "product/product.html", context)

def category_all(request):
    product = Product.objects.all()

     # مرتب سازی
    sort_by = request.GET.get('sort', 'default')  # مرتب‌سازی
    limit = int(request.GET.get('limit', 20))  # محدودیت نمایش

    # محصولات
    products = Product.objects.all()

    # مرتب‌سازی
    if sort_by == 'name_asc':
        products = products.order_by('title')
    elif sort_by == 'name_desc':
        products = products.order_by('-title')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'rating_desc':
        products = products.order_by('-rating')
    elif sort_by == 'rating_asc':
        products = products.order_by('rating')

    # محدودیت نمایش
    products = products[:limit]

    # صفحه بندی 
    paginator = Paginator(product, 12)  # 12 آیتم در هر صفحه

    # دریافت شماره صفحه از URL
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.filter(parent=None).prefetch_related('children')

    product_count_sold = Product.objects.filter(count_sold__gte=36).order_by('-count_sold')[:5]
    product_created_at = Product.objects.order_by('-created_at')[:5]
    special_products = Product.objects.filter(
        is_special=True).order_by('-discount')


    context = {
        "products": product,
        'sort_by': sort_by,
        'limit': limit,
        'page_obj': page_obj,
        'categories':categories,
        'product_count_sold':product_count_sold,
        'product_created_at':product_created_at,
        "special_products": special_products,


    }

    return render(request, 'product/category_all.html', context)


def category(request, slug):
    categories = Category.objects.filter(parent=None).prefetch_related('children')
    for category in categories:
        if not category.slug:
            category.slug = slugify(category.title)
            category.save()



    # مرتب سازی
    sort_by = request.GET.get('sort', 'default')  # مرتب‌سازی
    limit = int(request.GET.get('limit', 20))  # محدودیت نمایش


    product = Product.objects.all()
    category = get_object_or_404(Category, slug=slug)
    products = category.get_child_products().all()[:limit]
    



   

    # مرتب‌سازی
    if sort_by == 'name_asc':
        products = products.order_by('title')
    elif sort_by == 'name_desc':
        products = products.order_by('-title')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'rating_desc':
        products = products.order_by('-rating')
    elif sort_by == 'rating_asc':
        products = products.order_by('rating')

    

    # صفحه بندی 
    paginator = Paginator(product, 12)  # 12 آیتم در هر صفحه

    # دریافت شماره صفحه از URL
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    product_count_sold = Product.objects.filter(count_sold__gte=36).order_by('-count_sold')[:5]
    product_created_at = Product.objects.order_by('-created_at')[:5]
    special_products = Product.objects.filter(
        is_special=True).order_by('-discount')

    context = {
        "all_products": product,
        "products": products,
        "categorys": category,
        'sort_by': sort_by,
        'limit': limit,
        'page_obj': page_obj,
        'categories':categories,
        'special_products':special_products,
        'product_count_sold':product_count_sold,
        'product_created_at':product_created_at
        

    }

    return render(request, 'product/category.html', context)



def about_us(request):
    product_count_sold = Product.objects.filter(count_sold__gte=36).order_by('-count_sold')[:5]
    product_created_at = Product.objects.order_by('-created_at')[:5]
    special_products = Product.objects.filter(
        is_special=True).order_by('-discount')
    
    context = {
        'special_products':special_products,
        'product_count_sold':product_count_sold,
        'product_created_at':product_created_at,

    }

    return render(request, 'product/404.html', context)