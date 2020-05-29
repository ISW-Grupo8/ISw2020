from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy


from .models import Client
from .models import Product
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType

from products import custom
from .forms import UserCreateForm, ClientForm


# Create your views here.
APP_NAME = 'accessPermission'
APP_LABEL = 'accessPermission:'

class ClientCreateView(custom.ExtendUserCreateForm):
    model = User
    form_class = UserCreateForm
    child_model = Client
    child_form_class = ClientForm
    template_name = APP_NAME + '/client_create_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form, form_child):
        super(ClientCreateView, self).form_valid(form, form_child)

        self.object.groups.add(Group.objects.get(name='Clientes'))
        self.object.is_staff = False
        self.object.save()
        return redirect(self.get_success_url())