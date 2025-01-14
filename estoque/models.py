from django.db import models
from servicos.models import CategoriaManutencao

class Estoque(models.Model):
    nome = models.ForeignKey(CategoriaManutencao, on_delete=models.SET_NULL, null=True)
    quantidade_em_estoque = models.IntegerField()

    def __str__(self):
        return self.nome.titulo
