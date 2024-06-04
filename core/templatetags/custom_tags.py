from django import template

from core.models import Category, Cart
from core.utils import get_user_cart

register = template.Library()


@register.simple_tag()
def get_categories():
    categories = Category.objects.all()
    return categories


@register.simple_tag()
def user_carts(request):
    return get_user_cart(request)