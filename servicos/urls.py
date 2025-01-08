from django.urls import path
from django.contrib.auth.decorators import login_required
from servicos import views

urlpatterns = [
    path('novo_servico/', login_required(views.novo_servico, login_url='/login/'), name='novo_servico'),
    path('seleciona_servico/', login_required(views.editar_servico, login_url='/login/'), name='editar_servico'),
    path('editar_servico/', login_required(views.seleciona_servico, login_url='/login/'), name='seleciona_servico'),
    path('listar_servicos/', login_required(views.listar_servico, login_url='/login/'), name='listar_servico'),
    path('protocolo/<str:protocolo>', login_required(views.protocolo, login_url='/login/'), name='servico'),
    path('alterar_servico/<int:servico_id>', login_required(views.alterar_servico, login_url='/login/'), name='alterar_servico'),
    path("carros-por-cliente/<int:cliente_id>/", login_required(views.carros_por_cliente, login_url='/login/'), name="carros_por_cliente"),
]