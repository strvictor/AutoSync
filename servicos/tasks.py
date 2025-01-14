
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from servicos.models import Servicos
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from time import sleep


@shared_task
def valida_info_email(id_servico, caminho, assunto):
    sleep(10)
    # Obtém o serviço usando o ID
    servico_cliente = Servicos.objects.get(id=id_servico)

    contexto = {
        'titulo_servico': servico_cliente.titulo,
        'protocolo_servico': servico_cliente.protocolo,
        'nome': servico_cliente.cliente.nome,
        'sobrenome': servico_cliente.cliente.sobrenome,
        'email_cliente': servico_cliente.cliente.email,
        'carro': servico_cliente.carro.carro,
        'placa': servico_cliente.carro.placa,
        'servico': servico_cliente,
    }

    # Renderiza o e-mail
    html_content = render_to_string(caminho, contexto)
    text_content = strip_tags(html_content)

    send_mail(
        assunto,
        text_content,
        settings.EMAIL_HOST_USER,
        [contexto['email_cliente']],
        fail_silently=False,
        html_message=html_content
    )
    return f"\nE-mail enviado para:\nProtocolo: {servico_cliente.protocolo}\nNome: {servico_cliente.cliente.nome}\nE-mail: {servico_cliente.cliente.email}\n"
