from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from shop.models import Category, Product, Order, OrderEntry, Profile, Status
from django.contrib.auth import login, authenticate
from .forms import SignUpForm


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


def profile_cart_init(user):
    profile: Profile = Profile.objects.get_or_create(user=user)[0]
    if not profile.shopping_cart:
        profile.shopping_cart = (profile.orders.filter(status=Status.INITIAL).first()
                                 or Order.objects.create(profile=profile, status=Status.INITIAL))
        profile.save()

    return profile.shopping_cart


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    current_order = profile_cart_init(request.user)
    entry = OrderEntry.objects.get_or_create(order=current_order,
                                             product=product)[0]
    entry.count += 1
    entry.save()
    return redirect('shop:detail', product_id)


@login_required
def my_shopping_cart(request):
    profile: Profile = Profile.objects.filter(user=request.user).first()
    if (not profile.shopping_cart) or len(profile.shopping_cart.order_entries.all()) == 0:
        return render(request, 'shop/my_shopping_cart.html')

    entries = profile.shopping_cart.order_entries.all().order_by('-id')
    total_price = sum([(entry.product.price * entry.count) for entry in entries])
    return render(request, 'shop/my_shopping_cart.html', {'entries': entries,
                                                          'total_price': total_price})


@login_required
def shopping_cart_delete(request):
    profile: Profile = Profile.objects.filter(user=request.user).first()

    if profile.shopping_cart:
        profile.shopping_cart.delete()

    return redirect('shop:my_shopping_cart')


@login_required
def make_order(request):
    profile: Profile = Profile.objects.filter(user=request.user).first()

    order = profile.shopping_cart
    order.status = Status.COMPLETED
    order.save()

    profile.shopping_cart = None
    profile.save()

    return render(request, 'shop/make_order.html')
