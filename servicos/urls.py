from django.urls import path
from servicos import views

urlpatterns = [
    path('novo_servico/', views.novo_servico, name='novo_servico'),
    path('editar_servico/', views.editar_servico, name='editar_servico'),
    path('listar_servicos/', views.listar_servico, name='listar_servico'),
    path('protocolo/<str:protocolo>', views.protocolo, name='servico'),
    path('alterar_servico/<int:servico_id>', views.alterar_servico, name='alterar_servico'),
    path("carros-por-cliente/<int:cliente_id>/", views.carros_por_cliente, name="carros_por_cliente"),

]
