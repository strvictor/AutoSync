
from .models import PerfilUsuario

class EmpresaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.empresa = None

        if request.user.is_authenticated:
            try:
                request.empresa = request.user.perfil_usuario.empresa
            except PerfilUsuario.DoesNotExist:
                pass

        return self.get_response(request)
