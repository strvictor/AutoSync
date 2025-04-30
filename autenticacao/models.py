from django.contrib.auth.models import User
from django.db import models

class Empresa(models.Model):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True)
    nome_dono = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    telefone = models.CharField(max_length=15)


    def __str__(self):
        return f"{self.nome} - {self.nome_dono}"

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_usuario')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='usuarios_perfil')

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.empresa.nome}"