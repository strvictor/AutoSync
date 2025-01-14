from django.contrib import admin
from .models import Servicos, CategoriaManutencao, ServicoCategoriaQuantidade
from estoque.models import Estoque

class EstoqueInline(admin.TabularInline):
    model = Estoque
    fields = ('quantidade_em_estoque', 'atualizado_em')  # Campos visíveis no admin
    readonly_fields = ('atualizado_em',)  # Campos apenas para leitura

class CategoriaManutencaoAdmin(admin.ModelAdmin):
    inlines = [EstoqueInline]

class ServicosAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/filtrar_carros.js',)

admin.site.register(Servicos, ServicosAdmin)
admin.site.register(CategoriaManutencao, CategoriaManutencaoAdmin)
admin.site.register(ServicoCategoriaQuantidade)
