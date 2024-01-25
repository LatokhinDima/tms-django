from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from shop.models import Category, Product, Order, OrderEntry, Profile
from django.views.decorators.cache import cache_page
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.http import HttpRequest, Http404


def index(request):
    category_list = Category.objects.all()
    paginator = Paginator(category_list, 3)
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


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('page/')
    else:
        form = SignUpForm()
    return render(request, 'shop/registration.html', {'form': form})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    profile = Profile.objects.get(user=request.user)
    if not profile.shopping_cart:
        order = Order.objects.create(profile=profile)
        profile.shopping_cart = order
        profile.save()
    else:
        order = profile.shopping_cart
    order_entry, created = OrderEntry.objects.get_or_create(order=order, product=product)
    if not created:
        order_entry.count += 1
        order_entry.save()
    return redirect('shop:detail', product_id)


@login_required
def my_shopping_cart(request):
    categories = Category.objects.all()
    profile = Profile.objects.get(user=request.user)
    order = Order.objects.filter(profile=profile, status=Order.Status.INITIAL).first()
    if not order:
        order = Order.objects.create(profile=profile, status=Order.Status.INITIAL)
    entries = order.entries.all().order_by('product__id')
    total_amount = sum(entry.count * entry.product.price for entry in order.entries.all())
    return render(request, 'shop/my_shopping_cart.html',
                  {'order': order, 'total_amount': total_amount, 'categories': categories, 'entries': entries, })
