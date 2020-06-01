from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Fieldset, ButtonHolder

# Models
from .models import Category, Product, Publicity, Image, ProductDetail, Order, Card


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        helper.form_class = 'form-horizontal'
        helper.label_class = 'col-2'
        helper.field_class = 'col-10'
        # Hace que el boton de registrar del html funcione
        self.helper.form_tag = False

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        # Cambia el widget de la descripcion
        self.fields['description'].widget.attrs['rows'] = 3


class PublicityForm(forms.ModelForm):
    class Meta:
        model = Publicity
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PublicityForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.fields['description'].widget.attrs['rows'] = 3
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'name',
            'description',
            'image',
            HTML("""{% if form.image.value %}<img class='mb-2' src="/media/{{ form.image.value }}" width=420>{% endif %}""", ),
        )

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("image_file",)

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.form_tag = False
        # self.helper.layout = Layout(
        #     "image_file",
            # HTML(
            #     """{% if form.image_file.value %}<img class='mb-2' src="/media/{{ form.image_file.value }}" width=420>{% endif %} {{ form.image_file.value }}""", ),
        # )

class ProductDetailForm(forms.ModelForm):

    class Meta:
        model = ProductDetail
        fields = ("quantity",)

    def __init__(self, *args, **kwargs):
        super(ProductDetailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_tag = False


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(Card, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
