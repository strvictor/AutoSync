
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from servicos.models import Servicos
from celery import shared_task


@shared_task()
def valida_info_email(id_servico):
    # Obtém o serviço usando o ID
    servico_cliente = Servicos.objects.get(id=id_servico)

    # Cria o contexto para o template
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
    html_content = render_to_string('emails/template_email.html', contexto)
    text_content = strip_tags(html_content)

    assunto = 'Tudo pronto! Seu veículo está à sua espera 🚗'

    # Cria e envia o e-mail
    email = EmailMultiAlternatives(
        assunto,
        text_content,
        settings.EMAIL_HOST_USER,
        [contexto['email_cliente']],
    )
    email.attach_alternative(html_content, "text/html")
    
    email.send()
    print(f"\nE-mail enviado para:\nProtocolo: {servico_cliente.protocolo}\nNome: {servico_cliente.cliente.nome}\nE-mail: {servico_cliente.cliente.email}\n")
