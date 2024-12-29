from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('clientes/', include('clientes.urls')),
    path('servicos/', include('servicos.urls')),
    path('login/', include('autenticacao.urls')),

]
