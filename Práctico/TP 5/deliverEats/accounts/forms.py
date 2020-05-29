from django import forms

from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit


# Funciones para configurar crispy forms
def placeholder_as_label(object):
    # Paso el texto de las tags a los place holders
    # Debe estar creado el helper y el layout
    for field_name, field in object.fields.items():
        object.helper.layout.append(Field(field_name, placeholder=field.label))

def hide_help_text(object, exeptions=[]):
    # Oculta el texto de ayuda y lo guarda en el helper
    # Debe estar creado el helper
    object.helper.help_text = []
    for exeption in exeptions:
        # Guarda las exepciones bajo otro nombre para mostrarse mas comodamente
        object.helper.help_text.append(object.fields[exeption].help_text)

    for fieldname in object.fields:
        object.fields[fieldname].help_text = None


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()

        hide_help_text(self)
        placeholder_as_label(self)
        self.helper.form_tag = False