from django.contrib import admin
from .models import Servicos, CategoriaManutencao, ServicoCategoriaQuantidade

class ServicosAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/filtrar_carros.js',)

admin.site.register(Servicos, ServicosAdmin)
admin.site.register(CategoriaManutencao)
admin.site.register(ServicoCategoriaQuantidade)
