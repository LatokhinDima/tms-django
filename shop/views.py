from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from shop.models import Category, Product


def index(request):
    category_list = Category.objects.all()
    paginator = Paginator(category_list, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    Category.objects.prefetch_related(Product.__name__)
    return render(request, 'shop/index.html', {'categories': category_list, "page_obj": page_obj})


def detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/detail.html', {'product': product})


def category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category_id)
    context = {
        'products': products,
        'category': category
    }
    return render(request, 'shop/category.html', context)
