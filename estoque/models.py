from django.db import models
from servicos.models import CategoriaManutencao

     
class Estoque(models.Model):
    nome = models.OneToOneField(CategoriaManutencao, on_delete=models.SET_NULL, null=True)
    quantidade_em_estoque = models.IntegerField()
    quantidade_minima = models.IntegerField(null=True, blank=True, default=5)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nome.titulo} - {self.quantidade_em_estoque} em estoque'


class Reabastecimento(models.Model):
    item = models.ForeignKey(Estoque, on_delete=models.CASCADE, related_name='reabastecimentos')
    quantidade_adicionada = models.PositiveIntegerField()
    data_reabastecimento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.item.nome.titulo} - +{self.quantidade_adicionada} em {self.data_reabastecimento.strftime("%d/%m/%Y %H:%M")}'
