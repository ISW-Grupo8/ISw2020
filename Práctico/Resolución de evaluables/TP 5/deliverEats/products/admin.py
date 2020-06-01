from django.contrib import admin
from .models import Category, Product, Publicity, Image, ProductDetail

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Publicity)
admin.site.register(Image)
admin.site.register(ProductDetail)
