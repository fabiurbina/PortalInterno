from django.template.loader import render_to_string
from .email_ses import enviar_email


def enviar_email_boas_vindas(cliente, email, senha):

    contexto = {
        "razao_social": cliente["razao_social"],
        "login": cliente["cnpj_cpf"],
        "senha": senha,
        "portal": "https://portal.viesano.com.br/login/",
    }

    html = render_to_string(
        "emails/boas_vindas.html",
        contexto
    )

    enviar_email(
        assunto="Bem-vindo ao Portal do Cliente Viesano",
        destinatario=email,
        html=html
    )