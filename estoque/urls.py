from django.urls import path
from django.contrib.auth.decorators import login_required
from estoque import views

urlpatterns = [
    path('add-itens/', login_required(views.add_itens, login_url='/login/'), name='add_itens'),
]