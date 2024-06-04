from django.contrib.auth.models import User
from django.db import models
# from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Category')


    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Product Category', related_name='product')
    name = models.CharField(max_length=150, verbose_name='Product name')
    description = models.TextField(max_length=255, verbose_name='Description')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='url')
    image = models.ImageField(upload_to='images', verbose_name='Image')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Price')
    discount = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Discount')

    def __str__(self):
        return self.name

    def sell_price(self):
        return self.price

    def get_absolute_url(self):
        return reverse('detail', kwargs={'product_pk': self.pk})

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['id']


class TeamBlog(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Title')
    short_description = models.TextField(max_length=150, verbose_name='Short description')
    image = models.ImageField(upload_to='images', verbose_name='Image')

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title


class LoginForm(AuthenticationForm):
    class Meta:
        model = User


class CartQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, verbose_name='User')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Product')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Quantity')
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date the product was added')

    class Meta:
        db_table = 'cart'
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        ordering = ['id']

    objects = CartQueryset().as_manager()

    def products_price(self):
        return round(self.product.sell_price() * self.quantity)

    def __str__(self):
        return f'Cart {self.user.username} | Product {self.product.name} | Quantity {self.quantity}'



class WishItemQueryset(models.QuerySet):

    def total_price(self):
        return sum(wish_item.get_item_price() for wish_item in self)

    def total_quantity(self):
        if self:
            return sum(wish_item.quantity for wish_item in self)
        return 0


class WishItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, verbose_name='User')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

    objects = WishItemQueryset().as_manager()

    def get_item_price(self):
        return self.quantity * self.product.sell_price()



