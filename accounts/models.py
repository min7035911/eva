# accounts/models.py

import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from base.models import BaseModel
from products.models import FloorMatProduct
from home.models import ShippingAddress

class Profile(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    shipping_address = models.ForeignKey(
        ShippingAddress,
        on_delete=models.CASCADE,
        related_name="profiles",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username

    def get_cart_count(self):
        from .models import CartItem
        return CartItem.objects.filter(cart__is_paid=False, cart__user=self.user).count()

    def save(self, *args, **kwargs):
        # Remove old image file when updating
        if self.pk:
            try:
                old = Profile.objects.get(pk=self.pk)
                if old.profile_image and old.profile_image != self.profile_image:
                    old_path = os.path.join(settings.MEDIA_ROOT, old.profile_image.path)
                    if os.path.exists(old_path):
                        os.remove(old_path)
            except Profile.DoesNotExist:
                pass
        super().save(*args, **kwargs)


class Cart(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carts",
        null=True,
        blank=True
    )
    is_paid = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_signature = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Cart #{self.id} ({self.user})"

    def get_cart_total(self):
        total = 0
        for item in self.cart_items.all():
            total += item.get_product_price()
        return total


class CartItem(BaseModel):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="cart_items"
    )
    product = models.ForeignKey(
        FloorMatProduct, on_delete=models.SET_NULL, null=True, blank=True
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Позиция корзины"
        verbose_name_plural = "Позиции корзины"

    def __str__(self):
        return f"{self.quantity} × {self.product.code if self.product else '—'}"

    def get_product_price(self):
        if not self.product:
            return 0
        return self.product.get_price() * self.quantity
