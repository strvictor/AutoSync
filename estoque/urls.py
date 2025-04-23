from django.urls import path
from django.contrib.auth.decorators import login_required
from estoque.views import *

urlpatterns = [
    path('', login_required(estoque, login_url='/login/'), name='estoque'),
    path('reabastecer/', login_required(reabastecer_estoque, login_url='/login/'), name='reabastecer_estoque'),
]