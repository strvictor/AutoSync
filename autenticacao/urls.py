from django.urls import path
from autenticacao import views

urlpatterns = [
    path('', views.login_usuario, name='login_usuario'),
]
