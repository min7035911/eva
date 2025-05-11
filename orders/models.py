from django.db import models
from products.models import FloorMatProduct

class Order(models.Model):
    NEW, PROCESS, DONE = 'new','process','done'
    STATUS_CHOICES = [
        (NEW, 'Новый'),
        (PROCESS, 'В процессе'),
        (DONE, 'Завершён'),
    ]

    name    = models.CharField('Имя', max_length=64)
    phone   = models.CharField('Телефон', max_length=20)
    email   = models.EmailField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    status  = models.CharField(max_length=10, choices=STATUS_CHOICES, default=NEW)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'#{self.id} {self.name}'

class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(FloorMatProduct, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'
