from django.contrib import admin
from .models import Cart,Category, Order, OrderItem, MenuItem

# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)