from django import template
from django.db import models
from django.contrib.auth.models import Permission, User
from django.shortcuts import get_object_or_404
from products.models import Publicity
from django.db.models.aggregates import Count
import random

register = template.Library()

@register.filter
def verbose_name_plural(obj):
    return obj._meta.verbose_name_plural

@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name

@register.filter
def type(obj):
    return obj.__class__.__name__

@register.filter
def pronoun(obj):
    return obj._meta.pronoun

@register.filter
def field(obj, field_name):
    # Devuelve el valor del campo pasado por parametro
    if hasattr(obj, field_name):
        field = eval('obj.' + field_name)
        # Si el campo es un many to many devuelve todos los objetos
        if type(field) == 'ManyRelatedManager':
            field_list = field.all()
            list = []
            for i in field_list:
                list.append(str(i))
            return ', '.join(list)
        else:
            return field
    else:
        return ''

@register.simple_tag
def get_verbose_field_name(instance, field_name):
    # Returns verbose_name for a field.
    return instance._meta.get_field(field_name).verbose_name.title()

@register.filter
def has_perm_tag(user, perm):
    # Devuelve True si el usuario tiene el permiso pasado por parametro
    return user.has_perm(perm)

@register.filter
def get_redirect(obj, accion):
    # Concatena el nombre de la aplicacion la clase del objeto y su accion
    return obj.__module__.split('.')[0] + ':' + obj.__class__.__name__.lower() + '_' + accion

@register.filter
def create_url(obj):
    return get_redirect(obj, 'create')

@register.filter
def update_url(obj):
    return get_redirect(obj, 'update')

@register.filter
def delete_url(obj):
    return get_redirect(obj, 'delete')

@register.filter
def list_url(obj):
    return get_redirect(obj, 'list')

@register.filter
def detail_url(obj):
    return get_redirect(obj, 'detail')


# Devuelve True si el objeto tiene alguna imagen vinculada
@register.filter
def has_image(object):
    for img in object.image_set.all():
        if img.image_file != None: return True
    return False

@register.filter
def get_range(integer):
    return range(integer)

# Products
# Revisa que un usuario tenga los permisos adecuados
@register.filter
def has_perm(user, perm):
    return user.has_perm(perm)


@register.simple_tag
def show_publicity():
    count = Publicity.objects.all().count()
    if count == 0:
        return
    index = random.randint(0, count - 1)
    return Publicity.objects.all()[index].image

@register.filter()
def products_list_redirect(obj, user):
    object = obj.__class__.__name__.lower()
    if user.has_perm('products.change_' + object):
        return 'update'
    if user.has_perm('products.view_' + object):
        if type(obj) == 'Category':
            return ''
        else:
            return 'detail'
    return ''


@register.filter()
def products_list_delete(obj, user):
    object = obj.__class__.__name__.lower()
    if user.has_perm('products.change_' + object):
        return 'products/snippets/delete_button.html'
    return ''


@register.filter()
def products_list_create(obj, user):
    object = obj.__class__.__name__.lower()
    if user.has_perm('products.add_' + object):
        return True
    return False