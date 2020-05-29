from django.db import models
from django.contrib.auth.models import User, Group
from products.models import Product, ProductDetail
# Create your models here.


class Client(models.Model):
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario del cliente")
    shopping_cart = models.ManyToManyField(ProductDetail, related_name='shopping_cart', verbose_name="Carrito de compras")
    shopping_history = models.ManyToManyField(ProductDetail, related_name='shopping_history', verbose_name="Historial de compras")


    def __str__(self):
        return self.user.username

    @property
    def total(self):
        total = 0
        for product_detail in self.shopping_cart.all():
            total += product_detail.total
        return total

    def buy_all_items(self):
        for product_detail in self.shopping_cart.all():
            self.shopping_history.add(product_detail)
        self.shopping_cart.clear()