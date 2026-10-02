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
    
    
from django.urls import reverse
from django.conf import settings
from .models import ParticipanteReuniao


def enviar_convite_reuniao(reuniao, email):
    participante = ParticipanteReuniao.objects.get(
        reuniao=reuniao,
        email=email
    )

    base_url = settings.SITE_URL.rstrip("/")

    contexto = {
        "titulo": reuniao.titulo,
        "data": reuniao.inicio.strftime("%d/%m/%Y"),
        "hora_inicio": reuniao.inicio.strftime("%H:%M"),
        "hora_fim": reuniao.fim.strftime("%H:%M"),
        "organizador": reuniao.organizador_email,
        "descricao": reuniao.descricao or "Sem descrição.",
        "url_aceitar": f"{base_url}{reverse('responder_convite', args=[participante.token_resposta, 'aceitar'])}",
        "url_talvez": f"{base_url}{reverse('responder_convite', args=[participante.token_resposta, 'talvez'])}",
        "url_recusar": f"{base_url}{reverse('responder_convite', args=[participante.token_resposta, 'recusar'])}",
    }

    html = render_to_string(
        "emails/convite_reuniao.html",
        contexto
    )

    enviar_email(
        assunto=f"Convite para reunião: {reuniao.titulo}",
        destinatario=email,
        html=html
    )