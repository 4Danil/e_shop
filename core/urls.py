from django.urls import path

from . import views
from .views import get_category_product_view, WishListView, addToWishlist

urlpatterns = [
    path('', views.home_view, name='home'),
    path('search/', views.products_view, name='search'),
    path('about/', views.about_view, name='about'),
    path('products/', views.products_view, name='products'),

    path('wishlist/', WishListView.as_view(), name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', addToWishlist, name='add-to-wishlist'),
    path('wishlist_remove/<int:wishlist_id>/', views.wishlist_remove, name='wishlist_remove'),

    path('product/<int:product_pk>/', views.product_detail, name='detail'),
    path('categories/<int:category_id>/', get_category_product_view, name='category_products'),
    path('blog/', views.blogs_view, name='blog'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.registration_view, name='register'),

    path('cart/', views.users_cart, name='cart'),
    path('cart_add/<slug:product_slug>/', views.cart_add, name='cart_add'),
    # path('cart_change/<int:product_id>', views.cart_change, name='cart_change'),
    path('cart_remove/<int:cart_id>/', views.cart_remove, name='cart_remove'),
    path('increase_cart/<int:product_pk>/', views.increase_cart, name='increase'),
    path('decrease_cart/<int:product_pk>/', views.decrease_cart, name='decrease'),
]

# <int:cart_id>/