from django.db import models
from servicos.models import CategoriaManutencao

     
class Estoque(models.Model):
    empresa = models.ForeignKey('autenticacao.Empresa', on_delete=models.CASCADE)
    
    nome = models.OneToOneField(CategoriaManutencao, on_delete=models.CASCADE)
    quantidade_em_estoque = models.IntegerField(default=1)
    quantidade_minima = models.IntegerField(default=10)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nome.titulo} - {self.quantidade_em_estoque} em estoque'


class Reabastecimento(models.Model):
    empresa = models.ForeignKey('autenticacao.Empresa', on_delete=models.CASCADE)
    
    item = models.ForeignKey(Estoque, on_delete=models.CASCADE, related_name='reabastecimentos')
    quantidade_adicionada = models.PositiveIntegerField()
    data_reabastecimento = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.item.nome.titulo} - + {self.quantidade_adicionada} em {self.data_reabastecimento.strftime("%d/%m/%Y %H:%M")}'
