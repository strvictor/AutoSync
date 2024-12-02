from django.urls import path
from clientes import views

urlpatterns = [
    path('', views.clientes, name='clientes'),
    path('atualiza_cliente/', views.atualiza_cliente, name='atualiza_cliente'),
    path('atualiza_carro/<int:id_carro>', views.atualiza_carro, name='atualiza_carro'),
    path('update_cliente/<int:id_cliente>', views.update_cliente, name='update_cliente'),
]
