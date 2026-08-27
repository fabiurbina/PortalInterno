
import imaplib
import email
from email.message import Message
from datetime import datetime


IMAP_HOST = "imap.hostinger.com"
IMAP_PORT = 993


def extrair_ics(mensagem: Message):

    for parte in mensagem.walk():

        content_type = parte.get_content_type()

        if content_type in (
            "text/calendar",
            "application/ics"
        ):

            payload = parte.get_payload(
                decode=True
            )

            if not payload:
                continue

            charset = (
                parte.get_content_charset()
                or "utf-8"
            )

            return payload.decode(
                charset,
                errors="replace"
            )

    return None


def extrair_campo(ics, campo):

    for linha in ics.splitlines():

        if linha.startswith(campo + ":"):

            return linha.split(
                ":",
                1
            )[1].strip()

    return ""


def extrair_organizador(ics):

    for linha in ics.splitlines():

        if not linha.startswith("ORGANIZER"):
            continue

        nome = ""

        if "CN=" in linha:

            inicio = linha.find("CN=") + 3
            fim = linha.find(":", inicio)

            if fim != -1:
                nome = linha[inicio:fim]

        email_organizador = ""

        if "mailto:" in linha.lower():

            email_organizador = (
                linha.lower()
                .split("mailto:", 1)[1]
                .strip()
            )

        return nome, email_organizador

    return "", ""


def extrair_participantes(ics):

    participantes = []

    for linha in ics.splitlines():

        if not linha.startswith("ATTENDEE"):
            continue

        if "mailto:" not in linha.lower():
            continue

        email_participante = (
            linha.lower()
            .split("mailto:", 1)[1]
            .strip()
        )

        if email_participante not in participantes:

            participantes.append(
                email_participante
            )

    return participantes


def extrair_link_reuniao(ics):

    # Google Meet
    link = extrair_campo(
        ics,
        "X-GOOGLE-CONFERENCE"
    )

    if link:
        return link

    # Location
    location = extrair_campo(
        ics,
        "LOCATION"
    )

    if location:

        if "http://" in location or "https://" in location:
            return location

    # DESCRIPTION
    descricao = extrair_campo(
        ics,
        "DESCRIPTION"
    )

    for trecho in descricao.replace(
        "\\n",
        "\n"
    ).split():

        if trecho.startswith("https://"):

            if any(
                dominio in trecho.lower()
                for dominio in [
                    "meet.google.com",
                    "teams.microsoft.com",
                    "zoom.us",
                    "webex.com"
                ]
            ):
                return trecho

    return ""


def formatar_data(data):

    if not data:
        return ""

    try:

        data_limpa = data

        if data_limpa.endswith("Z"):
            data_limpa = data_limpa[:-1]

        dt = datetime.strptime(
            data_limpa,
            "%Y%m%dT%H%M%S"
        )

        return dt.strftime(
            "%d/%m/%Y %H:%M"
        )

    except Exception:

        return data


def processar_convite(mensagem):

    ics = extrair_ics(mensagem)

    if not ics:
        return None

    titulo = extrair_campo(
        ics,
        "SUMMARY"
    )

    inicio = extrair_campo(
        ics,
        "DTSTART;TZID=America/Sao_Paulo"
    )

    fim = extrair_campo(
        ics,
        "DTEND;TZID=America/Sao_Paulo"
    )

    if not inicio:
        inicio = extrair_campo(
            ics,
            "DTSTART"
        )

    if not fim:
        fim = extrair_campo(
            ics,
            "DTEND"
        )

    organizador_nome, organizador_email = (
        extrair_organizador(ics)
    )

    participantes = extrair_participantes(
        ics
    )

    link_reuniao = extrair_link_reuniao(
        ics
    )

    local = extrair_campo(
        ics,
        "LOCATION"
    )

    status = extrair_campo(
        ics,
        "STATUS"
    )

    uid = extrair_campo(
        ics,
        "UID"
    )

    descricao = extrair_campo(
        ics,
        "DESCRIPTION"
    )

    return {
        "uid": uid,
        "titulo": titulo,
        "inicio": inicio,
        "inicio_formatado": formatar_data(inicio),
        "fim": fim,
        "fim_formatado": formatar_data(fim),
        "organizador_nome": organizador_nome,
        "organizador_email": organizador_email,
        "participantes": participantes,
        "link_reuniao": link_reuniao,
        "local": local,
        "status": status,
        "descricao": descricao,
    }


def buscar_reunioes(email_usuario, senha):

    reunioes = []

    try:

        mail = imaplib.IMAP4_SSL(
            IMAP_HOST,
            IMAP_PORT
        )

        mail.login(
            email_usuario,
            senha
        )

        status, _ = mail.select(
            "INBOX"
        )

        if status != "OK":

            mail.logout()

            return {
                "sucesso": False,
                "erro": "Não foi possível acessar a caixa de entrada.",
                "reunioes": []
            }

        status, dados = mail.search(
            None,
            "BODY",
            '"BEGIN:VCALENDAR"'
        )

        if status != "OK":

            mail.logout()

            return {
                "sucesso": False,
                "erro": "Não foi possível pesquisar os e-mails.",
                "reunioes": []
            }

        candidatos = dados[0].split()

        for numero in reversed(candidatos):

            status, dados = mail.fetch(
                numero,
                "(RFC822)"
            )

            if status != "OK":
                continue

            status, dados = mail.fetch(
                numero,
                "(RFC822)"
            )

            if status != "OK":
                continue

            mensagem = email.message_from_bytes(
                dados[0][1]
            )

            reuniao = processar_convite(
                mensagem
            )

            if not reuniao:
                continue

            # Evita duplicidade pelo UID
            uid = reuniao["uid"]

            if uid and any(
                item["uid"] == uid
                for item in reunioes
            ):
                continue

            reunioes.append(
                reuniao
            )

        mail.logout()

        return {
            "sucesso": True,
            "erro": "",
            "reunioes": reunioes
        }

    except Exception as e:

        return {
            "sucesso": False,
            "erro": str(e),
            "reunioes": []
        }

