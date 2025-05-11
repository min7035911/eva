# products/models.py

from django.db import models
from django.urls import reverse

# Цветовые палитры
MAT_COLOR_CHOICES = [
    ("black", "Черный"), ("red", "Красный"), ("gray", "Серый"),
    ("navy", "Темно-синий"), ("brown", "Коричневый"), ("beige", "Бежевый"),
    ("blue", "Синий"), ("lime", "Салатовый"), ("violet", "Фиолетовый"),
    ("orange", "Оранжевый"),
]

BORDER_COLOR_CHOICES = MAT_COLOR_CHOICES[:]   # те же варианты


# --------------------------------------------------
# Автомобильные марки и модели
# --------------------------------------------------
class CarBrand(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Марка"
        verbose_name_plural = "Марки"

    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(CarBrand, related_name="models", on_delete=models.CASCADE)
    name = models.CharField("Модель", max_length=120)
    slug = models.SlugField(max_length=120)
    year_from = models.PositiveSmallIntegerField("Год с", blank=True, null=True)
    year_to   = models.PositiveSmallIntegerField("Год по", blank=True, null=True)

    class Meta:
        unique_together = ("brand", "slug")
        ordering = ["brand__name", "name"]
        verbose_name = "Модель"
        verbose_name_plural = "Модели"

    def __str__(self):
        return f"{self.brand} {self.name}"


# --------------------------------------------------
# Комплектация (опции)
# --------------------------------------------------
class InstallationOption(models.Model):
    name = models.CharField(max_length=80, unique=True)
    extra_price = models.PositiveIntegerField(default=0,
        help_text="Доплата в BYN за эту комплектацию")

    class Meta:
        ordering = ["id"]
        verbose_name = "Комплектация"
        verbose_name_plural = "Комплектации"

    def __str__(self):
        return f"{self.name} (+{self.extra_price} BYN)"


# --------------------------------------------------
# Коврики
# --------------------------------------------------
class FloorMatProduct(models.Model):
    code = models.CharField("Код товара", max_length=50, unique=True)
    name = models.CharField("Название", max_length=255)
    page_title = models.CharField("Title страницы", max_length=255, blank=True)
    price = models.DecimalField("Базовая цена", max_digits=8, decimal_places=2)

    short_description = models.CharField("Краткое описание", max_length=255)
    full_description  = models.TextField("Полное описание")
    meta_description  = models.CharField("Мета‑описание", max_length=160)

    car_model = models.ForeignKey(CarModel, on_delete=models.PROTECT, related_name="floor_mats")
    installation_options = models.ManyToManyField(InstallationOption, related_name="floor_mats", blank=True)

    mat_color    = models.CharField(max_length=24, choices=MAT_COLOR_CHOICES)
    border_color = models.CharField(max_length=24, choices=BORDER_COLOR_CHOICES)
    crossbar = models.BooleanField("Перемычка", default=False)
    heelpad  = models.BooleanField("Подпятник", default=False)

    image = models.ImageField(upload_to="floor_mats", blank=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["car_model__brand__name", "car_model__name"]
        verbose_name = "Коврик"
        verbose_name_plural = "Коврики"

    # -----------------------
    #  Бизнес‑логика
    # -----------------------
    EXTRA_CROSSBAR = 10
    EXTRA_HEELPAD = 20

    def get_price(self):
        """Цена с учётом опций crossbar/heelpad — без комплектации"""
        total = self.price
        if self.crossbar:
            total += self.EXTRA_CROSSBAR
        if self.heelpad:
            total += self.EXTRA_HEELPAD
        return total

    def __str__(self):
        return f"{self.code} – {self.name}"

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.pk])


# -----------------------------------------------
# Заглушки для старых импортов (временно)
# -----------------------------------------------
Product = FloorMatProduct
ColorVariant = None
SizeVariant = None
Coupon = None
