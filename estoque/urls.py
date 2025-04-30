from django.urls import path
from django.contrib.auth.decorators import login_required
from estoque.views import *

urlpatterns = [
    path('', login_required(estoque, login_url='/login/'), name='estoque'),
    path('reabastecer/', login_required(reabastecer_estoque, login_url='/login/'), name='reabastecer_estoque'),
    path('qtd-minima/', login_required(quantidade_minima, login_url='/login/'), name='quantidade_minima'),
    path('ultimos-reabastecimentos/', login_required(ultimos_reabastecimentos, login_url='/login/'), name='ultimos_reabastecimentos'),
    path('criar-item/', login_required(criar_item_estoque, login_url='/login/'), name='criar_item_estoque'),
]