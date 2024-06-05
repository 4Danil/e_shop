from django.contrib import auth, messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.views import generic

from .models import TeamBlog, Category, Product, Cart, WishItem
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm

# Create your views here.
from .utils import get_user_cart


def home_view(request):
    return render(request, 'core/home.html')


def about_view(request):
    return render(request, 'core/about.html')


class WishListView(generic.View):
    def get(self, *args, **kwargs):
        wish_items = WishItem.objects.filter(user=self.request.user)

        context = {
            'wish_items': wish_items
        }
        return render(self.request, 'core/wishlist.html', context)


def addToWishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        wish_items = WishItem.objects.filter(user=request.user, product=product)
        if wish_items.exists():
            wish_item = wish_items.first()
            if wish_item:
                wish_item.quantity += 1
                wish_item.save()

        else:
            WishItem.objects.create(user=request.user, product=product, quantity=1)

        return redirect(request.META['HTTP_REFERER'])
    return render(request, 'core/login.html')



def wishlist_remove(request, wishlist_id):
    wishlist = WishItem.objects.get(id=wishlist_id)
    wishlist.delete()

    return redirect(request.META['HTTP_REFERER'])


def products_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    search_query = request.GET.get('search', None)
    if search_query:
        products = Product.objects.filter(
            Q(name__icontains=search_query)
            |
            Q(description__icontains=search_query)
        )
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'core/products.html', context)


def get_category_product_view(request, category_id):
    category = Category.objects.get(pk=category_id)
    products = Product.objects.filter(category=category)
    context = {
        'products': products
    }
    return render(request, 'core/products.html', context)


def product_detail(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    context = {
        'product': product
    }
    return render(request, 'core/detail.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'core/login.html', context)


def registration_view(request):
    if request.method == 'POST':
        print(request.POST)
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'core/register.html', context)


def logout_view(request):
    logout(request)
    return render(request, 'core/home.html')


def blogs_view(request):
    blogs = TeamBlog.objects.all()
    context = {
        'blogs': blogs
    }
    return render(request, 'core/blogs.html', context)


def users_cart(request):
    return render(request, 'core/cart.html')


def cart_add(request, product_slug):
    product = Product.objects.get(slug=product_slug)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    return redirect(request.META['HTTP_REFERER'])


# def cart_change(request, product_id):
#     product = Product.objects.get(id=product_id)
#     if request.user.is_authenticated:
#         carts = Cart.objects.filter(user=request.user, product=product)
#
#         if carts:
#             cart = carts
#             if cart:
#                 cart.quantity += 1
#                 cart.save()
#         else:
#             Cart.objects.create(user=request.user, product=product, quantity=1)
#
#     return redirect(request.META['HTTP_REFERER'])


def cart_remove(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()

    return redirect(request.META['HTTP_REFERER'])


def increase_cart(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart.quantity >= 1:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    return redirect(request.META['HTTP_REFERER'])


def decrease_cart(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart.quantity > 1:
                cart.quantity -= 1
                cart.save()
        else:
            carts.remove(product)
            carts.delete()

    return redirect(request.META['HTTP_REFERER'])
