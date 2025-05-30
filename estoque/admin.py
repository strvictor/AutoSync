from django.contrib import admin
from estoque.models import *

class EstoqueAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.empresa:
            obj.empresa = request.user.perfil_usuario.empresa  # Define a empresa com base no usuário logado
        super().save_model(request, obj, form, change)

admin.site.register(Estoque, EstoqueAdmin)
admin.site.register(Reabastecimento)