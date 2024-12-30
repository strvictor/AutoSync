from django.urls import path
from django.contrib.auth.decorators import login_required
from home import views

urlpatterns = [
    path('', login_required(views.home, login_url='/login/'), name='home'),
]
