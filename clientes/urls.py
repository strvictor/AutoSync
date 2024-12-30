from django.urls import path
from django.contrib.auth.decorators import login_required
from clientes import views

urlpatterns = [
    path('', login_required(views.clientes, login_url='/login/'), name='clientes'),
    path('atualiza_cliente/', login_required(views.atualiza_cliente, login_url='/login/'), name='atualiza_cliente'),
    path('atualiza_carro/<int:id_carro>', login_required(views.atualiza_carro, login_url='/login/'), name='atualiza_carro'),
    path('update_cliente/<int:id_cliente>', login_required(views.update_cliente, login_url='/login/'), name='update_cliente'),
]
