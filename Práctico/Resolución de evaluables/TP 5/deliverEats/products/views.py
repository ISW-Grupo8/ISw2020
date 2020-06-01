from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from datetime import datetime
from django.db.models import Q
from operator import attrgetter

# Views
from django.views import generic
from . import custom
# Forms
from .forms import CategoryForm, ProductForm, PublicityForm, ImageForm, ProductDetailForm

# Models
from .models import Category, Product, Publicity, Image, ProductDetail

# Decorators
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
# Create your views here.

APP_NAME = 'products'
APP_LABEL = 'products:'

# Category
@method_decorator(permission_required('products.add_category'), name='dispatch')
class CategoryCreateView(custom.CustomCreateView):
    model = Category
    form_class = CategoryForm
    template_name = APP_NAME + '/create_form.html'
    success_url = reverse_lazy(APP_LABEL + 'category_list')


@method_decorator(permission_required('products.change_category'), name='dispatch')
class CategoryUpdateView(custom.CustomUpdateView):
    model = Category
    form_class = CategoryForm
    template_name = APP_NAME + '/update_form.html'


@method_decorator(permission_required('products.delete_category'), name='dispatch')
class CategoryDeleteView(custom.CustomDeleteView):
    model = Category
    masculine_pronoun = False
    template_name = APP_NAME + '/confirm_delete.html'


@method_decorator(permission_required('products.view_category'), name='dispatch')
class CategoryListView(custom.CustomListView):
    model = Category
    template_name = APP_NAME + '/list.html'
    fields = ['name']

    def get_queryset(self):
        return Category.objects.all().order_by('name')


# Product
# @method_decorator(permission_required('products.add_product'), name='dispatch')
class ProductCreateView(custom.MultipleModelCreateView):
    model = Product
    form_class = ProductForm
    child_model = Image
    child_form_class = ImageForm
    child_size = 5
    template_name = APP_NAME + '/create_form.html'
    success_url = reverse_lazy(APP_LABEL + 'product_list')


# @method_decorator(permission_required('products.change_product'), name='dispatch')
class ProductUpdateView(custom.MultipleModelUpdateView):
    model = Product
    form_class = ProductForm
    child_model = Image
    child_form_class = ImageForm
    child_size = 5
    template_name = APP_NAME + '/update_form.html'
    success_url = reverse_lazy(APP_LABEL + 'product_list')


@method_decorator(permission_required('products.delete_product'), name='dispatch')
class ProductDeleteView(custom.CustomDeleteView):
    model = Product
    template_name = APP_NAME + '/confirm_delete.html'


@method_decorator(permission_required('products.view_product'), name='dispatch')
class ProductListView(custom.CustomListView):
    model = Product
    template_name = APP_NAME + '/list.html'
    fields = ['name', 'price', 'stock', 'category']

    def get_queryset(self):
        return self.model.objects.all().order_by('name')


# Publicity
@method_decorator(permission_required('products.add_publicity'), name='dispatch')
class PublicityCreateView(custom.CustomCreateView):
    model = Publicity
    form_class = PublicityForm
    template_name = APP_NAME + '/create_form.html'
    success_url = reverse_lazy(APP_LABEL + 'publicity_list')


@method_decorator(permission_required('products.change_publicity'), name='dispatch')
class PublicityUpdateView(custom.CustomUpdateView):
    model = Publicity
    form_class = PublicityForm
    template_name = APP_NAME + '/update_form.html'


@method_decorator(permission_required('products.delete_publicity'), name='dispatch')
class PublicityDeleteView(custom.CustomDeleteView):
    model = Publicity
    template_name = APP_NAME + '/confirm_delete.html'


@method_decorator(permission_required('products.view_publicity'), name='dispatch')
class PublicityListView(custom.CustomListView):
    model = Publicity
    template_name = APP_NAME + '/list.html'
    fields = ['name', 'description']

    def get_queryset(self):
        return self.model.objects.all().order_by('name')

# Listas de objetos con barra de busqueda
def get_product_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        products = Product.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(category__name__icontains=q)
        )
        for product in products:
            queryset.append(product)

    return list(set(queryset))


# Ventas
class ProductSellListView(custom.CustomListView):
    model = Product
    template_name = APP_NAME + '/search_list.html'
    fields = ['name', 'price', 'description', 'category']

    def get_queryset(self):
        if self.request.GET:
            self.query = query = self.request.GET['q']
            # Ordena el query por nombre
            return sorted(get_product_queryset(query), key=attrgetter('name'), reverse=False)
        else:
            return self.model.objects.all().order_by('name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductSellListView, self).get_context_data(object_list=None, **kwargs)
        if self.request.GET:
            context['query'] = self.request.GET['q']
        return context


class ProductView(generic.CreateView):
    model = ProductDetail
    form_class = ProductDetailForm
    template_name = APP_NAME + '/product_detail.html'
    success_url = reverse_lazy(APP_LABEL + 'product_cart')

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data()
        # Se agrega el objeto del cual se hace la detail view, simulando un detail view
        context['object'] = get_object_or_404(Product, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        # Se crea un detalle de producto con la relacion al producto de la vista
        product_detail = ProductDetail(product=get_object_or_404(Product, pk=self.kwargs['pk']))
        # Se crea un formulario como instancia del del detalle del producto y se guarda
        form = ProductDetailForm(self.request.POST, instance=product_detail)
        product_detail = form.save()
        client = self.request.user.client
        # se agrega el detalle al carrito
        client.shopping_cart.add(product_detail)
        client.save()
        return redirect(self.success_url)


@method_decorator(permission_required('products.product_add_to_shopping_cart'), name='dispatch')
class CartListView(custom.CustomListView):
    model = ProductDetail
    template_name = APP_NAME + '/cart_list.html'

    def get_queryset(self):
        return self.request.user.client.shopping_cart.all()


@permission_required('products.product_add_to_shopping_cart')
@require_POST
def remove_product_from_cart(request, pk):
    product_detail = get_object_or_404(ProductDetail, pk=pk)
    client = request.user.client
    client.shopping_cart.remove(product_detail)
    client.save()
    return redirect(APP_LABEL + 'product_cart')


# todo ESTO HAY QUE REEMPLAZARLO
@permission_required('products.product_buy')
@require_POST
def buy_products_from_cart(request):
    client = request.user.client
    client.buy_all_items()
    return redirect(APP_LABEL + 'shopping_history_list')


@method_decorator(permission_required('products.product_buy'), name='dispatch')
class HistoryListView(custom.CustomListView):
    model = ProductDetail
    template_name = APP_NAME + '/history_list.html'

    def get_queryset(self):
        return self.request.user.client.shopping_history.all()


@method_decorator(permission_required('products.view_publicity'), name='dispatch')
class PublicityDetailView(generic.DetailView):
    model = Publicity
    template_name = APP_NAME + '/publicity_detail.html'

# TP5
class CreateOrderView(custom.CustomCreateView):
    pass

