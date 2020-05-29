from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy, resolve
from django.contrib.auth import authenticate, login

# Views
from django.views import generic, View

from django.forms.models import inlineformset_factory

# Custom generic views

# La vista agrega un objeto vacio para utilizar sus metadatos en la template
class CustomCreateView(generic.CreateView):
    template_name = 'custom/create_form.html'

    def get_context_data(self, **kwargs):
        # Agrego un objeto vacio para utilizar los datos de la clase meta
        context = super(CustomCreateView, self).get_context_data()
        context['object'] = self.model()
        return context


# La vista agrega un objeto vacio para utilizar sus metadatos en la template
# y al guardar el formulario lo vuelve a mostrar con un mensaje fr rcoyp
class CustomUpdateView(generic.UpdateView):
    template_name = 'custom/update_form.html'

    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data()
        context['success_message'] = 'Actualizado'
        context['form'] = self.get_form_class()(instance=self.object)
        context['object'] = self.object
        return render(self.request, self.template_name, context)


# La vista llama a la misma template al eliminar el objeto agregandole un mensaje de exito
class CustomDeleteView(generic.DeleteView):
    template_name = 'custom/confirm_delete.html'
    masculine_pronoun = True

    def get_context_data(self, **kwargs):
        context = super(CustomDeleteView, self).get_context_data()
        if self.masculine_pronoun: context['pronoun'] = 'el'
        else: context['pronoun'] = 'la'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        context['success_message'] = ' '
        self.object.delete()
        return render(request, self.template_name, context)


# La vista agrega una variable para los campos del objeto que se desea mostrar en la tabla
class CustomListView(generic.ListView):
    template_name = 'custom/list.html'
    fields = ['id']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CustomListView, self).get_context_data()
        context['object'] = self.model()
        context['fields'] = self.fields
        return context


# Permite crear un objeto de una clase y uno o varios objetos hijos vinculados a el
# Incorpora imagenes

class MultipleModelCreateView(generic.CreateView):
    template_name = 'custom/create_form.html'

    model = None
    form_class = None
    child_model = None
    child_form_class = None
    child_size = 1
    template_name = None
    # Helper que permite modifcar como se muestra el formset (opcional)
    formset_helper_class = None

    def get_formset_class(self, **kwargs):
        return inlineformset_factory(self.model, self.child_model, form=self.child_form_class, extra=self.child_size, max_num=self.child_size)

    def get_context_data(self, form=None, formset=None, **kwargs):
        # Se debe setear el objeto para que lo obtenga al llamar al metodo de la superclase
        self.object = self.model()
        # Devuelve los objetos form y object
        context = super(MultipleModelCreateView, self).get_context_data(**kwargs)
        if self.formset_helper_class: context['formset_helper'] = self.formset_helper_class()

        if self.request.POST:
            context['form'] = form
            context['formset'] = formset
        else:
            context['formset'] = self.get_formset_class()(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        formset = self.get_formset_class()(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object #Asi guarda la relacion al dni
        formset.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form, formset))


# Permite actualizar un objeto de una clase y uno o varios objetos hijos vinculados a el
class MultipleModelUpdateView(generic.UpdateView):
    model = None
    form_class = None
    child_model = None
    child_form_class = None
    child_size = 1
    template_name = None
    success_url = None
    formset_helper_class = None
    template_name = 'custom/update_form.html'


    def get_formset_class(self, **kwargs):
        return inlineformset_factory(self.model, self.child_model, form=self.child_form_class, extra=self.child_size, max_num=self.child_size)

    def get_context_data(self, success_msg=None, form=None, formset=None, **kwargs):
        # Devuelve los objetos form y object
        context = super(MultipleModelUpdateView, self).get_context_data(**kwargs)

        if success_msg: context['success_message'] = 'Actualizado'
        if self.formset_helper_class: context['formset_helper'] = self.formset_helper_class()

        if self.request.POST:
            if form: context['form'] = form
            else: context['form'] = self.get_form_class()(self.request.POST, self.request.FILES, instance=self.object)

            if formset: context['formset'] = formset
            else: context['formset'] = self.get_formset_class()(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = self.get_formset_class()(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = self.get_context_data()
        form = data['form']
        formset = data['formset']

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        print('form valid')
        form.save()
        formset.save()
        path = resolve(self.request.path_info).url_name
        # Se llama de nuevo a la funcion para evitar los errores que se muestran en la template
        # No muestra el mensaje de actualizado
        return redirect(self.object.__module__.split('.')[0] + ':' + path , pk=self.object.pk)
        # return render(self.request, self.template_name, self.get_context_data(success_msg='Actualizado'))

    def form_invalid(self, form, formset):
        print('form invalid')
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

class OneToOneCreateView(generic.CreateView):
    model = None
    form_class = None
    child_model = None
    child_form_class = None


    def get_context_data(self, form=None, form_child=None, **kwargs):
        # Se debe setear el objeto para que lo obtenga al llamar al metodo de la superclase
        self.object = self.model()
        # Devuelve los objetos form y object
        context = super(OneToOneCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            if form:
                context['form'] = form
            else:
                context['form'] = self.get_form_class()(self.request.POST)

            if form_child:
                context['form_child'] = form_child
            else:
                context['form_child'] = self.child_form_class(self.request.POST)

        else:
            context['form'] = self.get_form_class()()
            context['form_child'] = self.child_form_class()
        return context

    def post(self, request, *args, **kwargs):
        data = self.get_context_data()
        form = data['form']
        form_child = data['form_child']

        if form.is_valid() and form_child.is_valid():
            return self.form_valid(form, form_child)
        else:
            return self.form_invalid(form, form_child)

    def form_valid(self, form, form_child):
        self.object = form.save()
        # Crea un nuevo objeto sin setear los atributos y lo guarda
        self.child_object = self.child_model()
        # Guarda la relacion al objeto padre
        setattr(self.child_object, self.model().__class__.__name__.lower(), self.object)
        # Crea el formulario como instancia del objeto creado y lo guarda
        form_child = self.child_form_class(self.request.POST, instance=self.child_object).save()
        return redirect(self.get_success_url())

    def form_invalid(self, form, form_child):
        return self.render_to_response(self.get_context_data(form, form_child))


# View que crea a un usuario y al objeto que extiende de el logeando al usuario al finalizar
class ExtendUserCreateForm(OneToOneCreateView):
    def form_valid(self, form, form_child):
        super(ExtendUserCreateForm, self).form_valid(form, form_child)
        # Logea al usuario al finalizar
        login(self.request, self.object)
        return redirect(self.get_success_url())

# Permite actualizar un objeto de una clase junto a otro objeto vinculado a el
class OneToOneUpdateView(generic.UpdateView):
    model = None
    form_class = None
    child_model = None
    child_form_class = None

    def get_child_object(self):
        return getattr(self.get_object(), self.child_model().__class__.__name__.lower())

    def get_context_data(self, success_msg=None, form=None, form_child=None, **kwargs):
        # Devuelve los objetos form y object
        context = {}
        self.object, self.child_object = self.get_object(), self.get_child_object()
        if success_msg: context['success_message'] = 'Actualizado'

        if self.request.POST:
            if form: context['form'] = form
            else: context['form'] = self.get_form_class()(self.request.POST, instance=self.object)

            if form_child: context['form_child'] = form_child
            else: context['form_child'] = self.child_form_class(self.request.POST, instance=self.child_object)
        else:
            context['form'] = self.get_form_class()(instance=self.object)
            context['form_child'] = self.child_form_class(instance=self.child_object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = self.get_context_data()
        form = data['form']
        form_child = data['form_child']

        if form.is_valid() and form_child.is_valid():
            return self.form_valid(form, form_child)
        else:
            return self.form_invalid(form, form_child)

    def form_valid(self, form, form_child):
        form.save()
        form_child.save()
        return render(self.request, self.template_name, self.get_context_data(success_msg='Actualizado'))

    def form_invalid(self, form, form_child):
        return self.render_to_response(self.get_context_data(form=form, form_child=form_child))
