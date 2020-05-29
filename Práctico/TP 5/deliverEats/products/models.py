from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.


class Product(models.Model):
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        permissions = [
            ("product_buy", "Puede comprar un producto"),
            ("product_add_to_shopping_cart", "Puede agregar un producto al carrito"),
        ]

    name = models.CharField(u'Nombre', max_length=256)
    description = models.TextField(u"Descripción", null=True, blank=True)
    category = models.ManyToManyField('Category', verbose_name="Categorías")
    price = models.DecimalField(u"Precio", max_digits=5, decimal_places=2)
    stock = models.PositiveIntegerField(u"Stock", default=0)

    def __str__(self):
        return self.name


class ProductDetail(models.Model):
    class Meta:
        verbose_name = 'Detalle de producto'
        verbose_name_plural = 'Detalles de productos'

    product = models.ForeignKey("Product", verbose_name="Producto", on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(u"cantidad", validators=[MinValueValidator(1)])

    def __str__(self):
        return self.product.name

    @property
    def total(self):
        return self.product.price * self.quantity



class Category(models.Model):
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    name = models.CharField(u'Nombre', max_length=256)

    def __str__(self):
        return self.name


class Publicity(models.Model):
    class Meta:
        verbose_name = "Anuncio publicitario"
        verbose_name_plural = "Anuncios publicitarios"

    name = models.CharField(u'Nombre', max_length=256)
    description = models.TextField(u"Descripción", null=True, blank=True)
    image = models.ImageField(u"Imagen", upload_to='publicity_image', null=True, blank=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    image_file = models.ImageField(u"Imagen", upload_to='product_image')
    product = models.ForeignKey("Product", on_delete=models.CASCADE, verbose_name="Producto")

    def __str__(self):
        return self.product.name


class Order(models.Model):
    CITY_CHOICES = ((1, "Córdoba"), (2, "Río Cuarto"), (3, "Oncativo"), (4, "CarlosPaz"), (5, "Alta Gracia"),
                    (6, "Villa General Belgrano"), (7, "Río Tercero"), (8, "Villa Giardino"), (9, "Oliva"),
                    (10, "Río Segundo"))
    city = models.PositiveIntegerField(u'Ciudad', choices=CITY_CHOICES)
    street = models.CharField(u'Calle', max_length=40)
    street_number = models.CharField(u'Numero', max_length=10)
    reference = models.TextField(u'referencia', max_length=100, null=True, blank=True)

#     Forma de pago
    PAYMENT_METHOD = (('E', 'Efectivo'), ('T', 'Tarjeta'))
    payment_method = models.CharField(u'Metodo de pago', choices=PAYMENT_METHOD, max_length=1)
    immediate_delivery = models.BooleanField('Recibir lo antes posible')
    delivery_time = models.DateTimeField(u'Fecha y hora de entrega')


class Card(models.Model):
    order = models.OneToOneField('Order', name="Orden", on_delete=models.CASCADE)
    number = models.PositiveIntegerField(u'Numero de tarjeta')
    name = models.CharField(u'Nombre del titular', max_length=40)
    surname = models.CharField(u'Apellido del titular', max_length=40)
    due_date = models.DateField(u'Fecha de vencimiento')
    cvc = models.PositiveIntegerField(u'CVC')
