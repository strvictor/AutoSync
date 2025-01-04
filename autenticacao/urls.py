from django.urls import path
from autenticacao import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.login_usuario, name='login_usuario'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

]
