from django.urls import path
from .views import \
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView, CategoryListView, \
    ProductCreateView, ProductUpdateView, ProductDeleteView, ProductListView,\
    ProductSellListView, ProductView, CartListView, remove_product_from_cart, \
    buy_products_from_cart, HistoryListView, \
    PublicityCreateView, PublicityUpdateView, PublicityDeleteView, PublicityListView, PublicityDetailView

app_name = 'products'

urlpatterns = [
    # Category
    path('category/create', CategoryCreateView.as_view(), name='category_create'),
    path('category/change/<int:pk>', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>', CategoryDeleteView.as_view(), name='category_delete'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    # Product
    path('product/create', ProductCreateView.as_view(), name='product_create'),
    path('product/change/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete'),
    path('product/', ProductListView.as_view(), name='product_list'),
    # Client-side
    path('product/sell', ProductSellListView.as_view(), name='product_sell_list'),
    path('product/<int:pk>', ProductView.as_view(), name='product_detail'),
    path('product/shopping_cart', CartListView.as_view(), name='product_cart'),
    path('product/remove_from_cart/<int:pk>', remove_product_from_cart, name='product_remove_form_cart'),
    path('product/buy_products', buy_products_from_cart, name='buy_products_from_cart'),
    path('product/shopping_history', HistoryListView.as_view(), name='shopping_history_list'),

    # Publicity
    path('publicity/create', PublicityCreateView.as_view(), name='publicity_create'),
    path('publicity/change/<int:pk>', PublicityUpdateView.as_view(), name='publicity_update'),
    path('publicity/delete/<int:pk>', PublicityDeleteView.as_view(), name='publicity_delete'),
    path('publicity/', PublicityListView.as_view(), name='publicity_list'),
    path('publicity/<int:pk>', PublicityDetailView.as_view(), name='publicity_detail'),

]