from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Servicos
from .commands import EnviaEmail
from time import sleep

@receiver(post_save, sender=Servicos)
def teste(sender, instance, created, **kwargs):

    if created:
        print(f"Objeto criado: {instance}")
        sleep(10)
        envia_email = EnviaEmail()
        envia_email.trata_emails(instance.id)  # Usa o ID da instância criada
