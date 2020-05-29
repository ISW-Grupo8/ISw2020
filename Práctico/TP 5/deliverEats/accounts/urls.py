from django.urls import path
from django.contrib.auth import views as auth_views
from .views import AccountUpdateView

app_name = 'accounts'
urlpatterns = [
    path('account/', AccountUpdateView.as_view(), name="account_update"),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

    # Se modifica logout para que apunte al indice del sitio
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Se incluyen todas las views de django

    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change_form.html',
        success_url='/accounts/password_change/done/'),
         name='password_change',),
]
