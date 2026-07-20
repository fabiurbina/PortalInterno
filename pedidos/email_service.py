from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.conf import settings


def enviar_email_boas_vindas(cliente, email, senha):
    
    print("HOST:", settings.EMAIL_HOST)
    print("PORTA:", settings.EMAIL_PORT)
    print("USUARIO:", settings.EMAIL_HOST_USER)
    

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

    mensagem = EmailMultiAlternatives(
        subject="Bem-vindo ao Portal do Cliente Viesano",
        body="Seu e-mail não suporta HTML.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email]
    )

    mensagem.attach_alternative(html, "text/html")
    
    

    mensagem.send(fail_silently=False)