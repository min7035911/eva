# accounts/admin.py

from django.contrib import admin
from .models import Profile, Cart, CartItem

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_email_verified')
    search_fields = ('user__username', 'user__email')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_paid', 'created')
    list_filter = ('is_paid',)
    search_fields = ('user__username',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('product__code', 'cart__user__username')
