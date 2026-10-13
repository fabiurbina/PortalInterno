
import imaplib
import email
from email.message import Message
from datetime import datetime
import re
from django.db import transaction
from ..models import ReuniaoAgenda

# ============================================================
# CONFIGURAÇÃO IMAP
# ============================================================

IMAP_HOST = "imap.hostinger.com"
IMAP_PORT = 993


# ============================================================
# EXTRAIR ICS
# ============================================================

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


# ============================================================
# NORMALIZAR ICS
# ============================================================

def normalizar_ics(ics):

    # Remove quebra de linha usada para
    # continuar uma propriedade do ICS.
    ics = re.sub(
        r"\r?\n[ \t]",
        "",
        ics
    )

    return ics


# ============================================================
# EXTRAIR CAMPO SIMPLES
# ============================================================

def extrair_campo(ics, campo):

    ics = normalizar_ics(ics)

    for linha in ics.splitlines():

        if linha.startswith(campo + ":"):

            return linha.split(
                ":",
                1
            )[1].strip()

    return ""


# ============================================================
# EXTRAIR CAMPO COM PARÂMETROS
# ============================================================

def extrair_campo_parametrizado(
    ics,
    campo
):

    ics = normalizar_ics(ics)

    for linha in ics.splitlines():

        if linha.startswith(campo + ";"):

            partes = linha.split(
                ":",
                1
            )

            if len(partes) == 2:

                return partes[1].strip()

    return ""


# ============================================================
# EXTRAIR ORGANIZADOR
# ============================================================

def extrair_organizador(ics):

    ics = normalizar_ics(ics)

    for linha in ics.splitlines():

        if not linha.startswith(
            "ORGANIZER"
        ):
            continue

        nome = ""

        match_nome = re.search(
            r"CN=([^:;]+)",
            linha
        )

        if match_nome:

            nome = (
                match_nome.group(1)
                .strip()
            )

        email_organizador = ""

        match_email = re.search(
            r"mailto:([^;\s]+)",
            linha,
            re.IGNORECASE
        )

        if match_email:

            email_organizador = (
                match_email.group(1)
                .strip()
                .lower()
            )

        return (
            nome,
            email_organizador
        )

    return "", ""


# ============================================================
# EXTRAIR PARTICIPANTES
# ============================================================

def extrair_participantes(ics):

    participantes = []

    ics = normalizar_ics(ics)

    for linha in ics.splitlines():

        if not linha.startswith(
            "ATTENDEE"
        ):
            continue

        match = re.search(
            r"mailto:([^;\s]+)",
            linha,
            re.IGNORECASE
        )

        if not match:
            continue

        participante = (
            match.group(1)
            .strip()
            .lower()
        )

        if participante not in participantes:

            participantes.append(
                participante
            )

    return participantes


# ============================================================
# EXTRAIR LINK DA REUNIÃO
# ============================================================

def extrair_link_reuniao(ics):

    ics = normalizar_ics(ics)

    # --------------------------------------------------------
    # PROCURA DIRETAMENTE NO ICS
    # --------------------------------------------------------

    padroes = [
        "https://meet.google.com/",
        "https://teams.microsoft.com/",
        "https://zoom.us/",
        "https://webex.com/",
        "https://www.webex.com/",
    ]

    for linha in ics.splitlines():

        for padrao in padroes:

            if padrao in linha:

                inicio = linha.find(
                    padrao
                )

                link = linha[inicio:]

                link = re.split(
                    r"[\\\s<>]",
                    link
                )[0]

                return link.rstrip(
                    ".,;)"
                )

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    location = extrair_campo(
        ics,
        "LOCATION"
    )

    if location:

        match = re.search(
            r"https?://[^\s\\<>]+",
            location,
            re.IGNORECASE
        )

        if match:

            return (
                match.group(0)
                .rstrip(".,;)")
            )

    # --------------------------------------------------------
    # DESCRIPTION
    # --------------------------------------------------------

    descricao = extrair_campo(
    ics,
    "DESCRIPTION"
    )

    descricao = (
        descricao
        .replace("\\n", "\n")
        .replace("\\,", ",")
        .replace("\\;", ";")
        .strip()
    )

    if descricao.upper() in ("REMINDER", "REMINDER:"):
        descricao = ""

    # ========================================================
    # LIMPAR LIXO COMUM DE CONVITES OUTLOOK / TEAMS
    # ========================================================

    linhas_descricao = []

    for linha in descricao.splitlines():

        linha_limpa = linha.strip()

        if not linha_limpa:
            continue

        # Ignora textos técnicos do convite
        if linha_limpa.upper() in (
            "REMINDER",
            "REMINDER:",
        ):
            continue

        linhas_descricao.append(
            linha_limpa
        )

    descricao = "\n".join(
        linhas_descricao
    ).strip()

    match = re.search(
        r"https?://[^\s\\<>]+",
        descricao,
        re.IGNORECASE
    )

    if match:

        link = (
            match.group(0)
            .rstrip(".,;)")
        )

        if any(
            dominio in link.lower()
            for dominio in [
                "meet.google.com",
                "teams.microsoft.com",
                "zoom.us",
                "webex.com"
            ]
        ):

            return link

    return ""


# ============================================================
# CONVERTER DATA DO ICS
# ============================================================

def converter_data_ics(data):

    if not data:
        return None

    data = data.strip()

    formatos = [
        "%Y%m%dT%H%M%S",
        "%Y%m%dT%H%M%SZ",
        "%Y%m%d",
    ]

    for formato in formatos:

        try:

            return datetime.strptime(
                data,
                formato
            )

        except ValueError:

            continue

    return None


# ============================================================
# FORMATAR DATA
# ============================================================

def formatar_data(data):

    dt = converter_data_ics(
        data
    )

    if not dt:
        return data or ""

    return dt.strftime(
        "%d/%m/%Y %H:%M"
    )
    
    
# ============================================================
# EXTRAIR LINK DO CORPO DO E-MAIL
# ============================================================

def extrair_link_email(mensagem):

    try:

        if mensagem.is_multipart():

            partes = mensagem.walk()

            for parte in partes:

                content_type = parte.get_content_type()

                if content_type == "text/html":

                    payload = parte.get_payload(
                        decode=True
                    )

                    if not payload:
                        continue

                    html = payload.decode(
                        "utf-8",
                        errors="ignore"
                    )

                    match = re.search(
                        r'https?://[^"\s<>]+',
                        html,
                        re.IGNORECASE
                    )

                    if match:

                        link = match.group(0)

                        if any(
                            dominio in link.lower()
                            for dominio in [
                                "teams.live.com",
                                "teams.microsoft.com",
                                "meet.google.com",
                                "zoom.us",
                                "webex.com"
                            ]
                        ):

                            return link.rstrip(
                                '.,);"\'>'
                            )

        else:

            payload = mensagem.get_payload(
                decode=True
            )

            if payload:

                html = payload.decode(
                    "utf-8",
                    errors="ignore"
                )

                match = re.search(
                    r'https?://[^"\s<>]+',
                    html,
                    re.IGNORECASE
                )

                if match:

                    link = match.group(0)

                    if any(
                        dominio in link.lower()
                        for dominio in [
                            "teams.live.com",
                            "teams.microsoft.com",
                            "meet.google.com",
                            "zoom.us",
                            "webex.com"
                        ]
                    ):

                        return link.rstrip(
                            '.,);"\'>'
                        )

    except Exception:

        pass

    return ""


# ============================================================
# PROCESSAR CONVITE
# ============================================================

def processar_convite(mensagem):

    ics = extrair_ics(
        mensagem
    )

    if not ics:
        return None

    ics = normalizar_ics(
        ics
    )

    titulo = extrair_campo(
        ics,
        "SUMMARY"
    )

    # --------------------------------------------------------
    # INÍCIO
    # --------------------------------------------------------

    inicio = extrair_campo_parametrizado(
        ics,
        "DTSTART"
    )

    if not inicio:

        inicio = extrair_campo(
            ics,
            "DTSTART"
        )

    # --------------------------------------------------------
    # FIM
    # --------------------------------------------------------

    fim = extrair_campo_parametrizado(
        ics,
        "DTEND"
    )

    if not fim:

        fim = extrair_campo(
            ics,
            "DTEND"
        )

    # --------------------------------------------------------
    # DATA
    # --------------------------------------------------------

    dt_inicio = converter_data_ics(
        inicio
    )

    dt_fim = converter_data_ics(
        fim
    )

    if not dt_inicio:

        return None

    # --------------------------------------------------------
    # ORGANIZADOR
    # --------------------------------------------------------

    (
        organizador_nome,
        organizador_email
    ) = extrair_organizador(
        ics
    )

    # --------------------------------------------------------
    # PARTICIPANTES
    # --------------------------------------------------------

    participantes = (
        extrair_participantes(
            ics
        )
    )

    # --------------------------------------------------------
    # LINK
    # --------------------------------------------------------

    link_reuniao = (
    extrair_link_reuniao(
        ics
    )
    )

    if not link_reuniao:

        link_reuniao = (
            extrair_link_email(
                mensagem
            )
        )

    # --------------------------------------------------------
    # OUTROS DADOS
    # --------------------------------------------------------

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

    descricao = (
        descricao
        .replace("\\n", "\n")
        .replace("\\,", ",")
    )

    # --------------------------------------------------------
    # EVENTO
    # --------------------------------------------------------

    return {

        "uid": uid,

        "titulo": (
            titulo
            or "Reunião"
        ),

        "inicio": inicio,

        "fim": fim,

        "inicio_formatado": (
            formatar_data(
                inicio
            )
        ),

        "fim_formatado": (
            formatar_data(
                fim
            )
        ),

        "data": dt_inicio.strftime(
            "%Y-%m-%d"
        ),

        "hora_inicio": (
            dt_inicio.strftime(
                "%H:%M"
            )
            if "T" in inicio
            else ""
        ),

        "hora_fim": (
            dt_fim.strftime(
                "%H:%M"
            )
            if dt_fim and "T" in fim
            else ""
        ),

        "organizador_nome": (
            organizador_nome
        ),

        "organizador_email": (
            organizador_email
        ),

        "participantes": (
            participantes
        ),

        "link_reuniao": (
            link_reuniao
        ),

        "local": local,

        "status": status,

        "descricao": descricao,
    }


# ============================================================
# BUSCAR REUNIÕES
# ============================================================

# ============================================================
# SINCRONIZAR REUNIÕES COM O BANCO
# ============================================================

def sincronizar_reunioes(
    conta,
    reunioes
):

    quantidade = 0

    with transaction.atomic():

        for reuniao in reunioes:

            uid = reuniao.get(
                "uid",
                ""
            ).strip()

            if not uid:
                continue

            inicio = converter_data_ics(
                reuniao.get("inicio", "")
            )

            fim = converter_data_ics(
                reuniao.get("fim", "")
            )

            data_evento = None

            if inicio:

                data_evento = inicio.date()

            dados = {

                "titulo": reuniao.get(
                    "titulo",
                    ""
                ),

                "inicio": inicio,

                "fim": fim,

                "inicio_formatado": reuniao.get(
                    "inicio_formatado",
                    ""
                ),

                "fim_formatado": reuniao.get(
                    "fim_formatado",
                    ""
                ),

                "data": data_evento,

                "hora_inicio": reuniao.get(
                    "hora_inicio",
                    ""
                ),

                "hora_fim": reuniao.get(
                    "hora_fim",
                    ""
                ),

                "organizador_nome": reuniao.get(
                    "organizador_nome",
                    ""
                ),

                "organizador_email": reuniao.get(
                    "organizador_email",
                    ""
                ),

                "participantes": reuniao.get(
                    "participantes",
                    []
                ),

                "link_reuniao": reuniao.get(
                    "link_reuniao",
                    ""
                ),

                "local": reuniao.get(
                    "local",
                    ""
                ),

                "status": reuniao.get(
                    "status",
                    ""
                ),

                "descricao": reuniao.get(
                    "descricao",
                    ""
                ),

            }

            ReuniaoAgenda.objects.update_or_create(

                conta=conta,

                uid=uid,

                defaults=dados

            )

            quantidade += 1

    return quantidade

# ============================================================
# SINCRONIZAR TODAS AS CONTAS HOSTINGER
# ============================================================

def sincronizar_todas_agendas():

    from ..models import ContaHostinger
    from ..views import descriptografar_senha_hostinger

    resultados = []

    contas = ContaHostinger.objects.all()

    for conta in contas:

        try:

            senha = descriptografar_senha_hostinger(
                conta.senha_criptografada
            )

            resultado = buscar_reunioes(
                conta.email,
                senha,
                conta=conta
            )

            resultados.append({

                "usuario": conta.usuario.username,

                "email": conta.email,

                "sucesso": resultado["sucesso"],

                "quantidade": len(
                    resultado.get(
                        "reunioes",
                        []
                    )
                ),

                "erro": resultado.get(
                    "erro",
                    ""
                ),

            })

        except Exception as e:

            resultados.append({

                "usuario": conta.usuario.username,

                "email": conta.email,

                "sucesso": False,

                "quantidade": 0,

                "erro": str(e),

            })

    return resultados

def buscar_reunioes(
    email_usuario,
    senha,
    conta=None
):

    reunioes = []

    mail = None

    try:

        print(
            "🔌 Conectando à Hostinger..."
        )

        mail = imaplib.IMAP4_SSL(
            IMAP_HOST,
            IMAP_PORT
        )

        mail.login(
            email_usuario,
            senha
        )

        print(
            "✅ Conectado!"
        )

        # ----------------------------------------------------
        # ABRIR INBOX
        # ----------------------------------------------------

        status, _ = mail.select(
            "INBOX"
        )

        if status != "OK":

            return {
                "sucesso": False,
                "erro": (
                    "Não foi possível acessar "
                    "a caixa de entrada."
                ),
                "reunioes": []
            }

        # ----------------------------------------------------
        # PESQUISA INTELIGENTE
        # ----------------------------------------------------
        #
        # Primeiro tentamos localizar mensagens que
        # contenham indicadores típicos de convite.
        #
        # Não fazemos fetch de todos os e-mails.
        #
        # ----------------------------------------------------

        buscas = [

            (
                "BODY",
                '"BEGIN:VCALENDAR"'
            ),

            (
                "SUBJECT",
                '"Convite"'
            ),

            (
                "SUBJECT",
                '"Invitation"'
            ),

            (
                "SUBJECT",
                '"Reunião"'
            ),

            (
                "SUBJECT",
                '"Meeting"'
            ),

            (
                "SUBJECT",
                '"Calendar"'
            ),

        ]

        candidatos = set()

        for criterio, valor in buscas:

            try:

                status, dados = mail.search(
                    None,
                    criterio,
                    valor
                )

                if status != "OK":
                    continue

                if not dados:
                    continue

                for numero in dados[0].split():

                    candidatos.add(
                        numero
                    )

            except Exception:

                continue

        # ----------------------------------------------------
        # CASO A BUSCA NÃO RETORNE NADA
        # ----------------------------------------------------

        if not candidatos:

            mail.logout()

            return {
                "sucesso": True,
                "erro": "",
                "reunioes": []
            }

        print(
            f"📨 Mensagens candidatas: "
            f"{len(candidatos)}"
        )

        # ----------------------------------------------------
        # BAIXAR SOMENTE CANDIDATOS
        # ----------------------------------------------------

        for numero in reversed(
            list(candidatos)
        ):

            try:

                status, dados = mail.fetch(
                    numero,
                    "(RFC822)"
                )

                if status != "OK":
                    continue

                mensagem = None

                for item in dados:

                    if (
                        isinstance(item, tuple)
                        and len(item) > 1
                    ):

                        mensagem = (
                            email.message_from_bytes(
                                item[1]
                            )
                        )

                        break

                if not mensagem:
                    continue

                reuniao = (
                    processar_convite(
                        mensagem
                    )
                )

                # ------------------------------------------------
                # CONFIRMA QUE É REALMENTE UM ICS
                # ------------------------------------------------

                if not reuniao:
                    continue

                # ------------------------------------------------
                # EVITAR DUPLICIDADE
                # ------------------------------------------------

                uid = reuniao["uid"]

                if uid:

                    if any(
                        item["uid"] == uid
                        for item in reunioes
                    ):

                        continue

                reunioes.append(
                    reuniao
                )

            except Exception:

                continue

        # ----------------------------------------------------
        # ORDENAR
        # ----------------------------------------------------

        reunioes.sort(
            key=lambda item: (
                item["data"],
                item["hora_inicio"]
            )
        )

        print(
            f"📅 Reuniões encontradas: "
            f"{len(reunioes)}"
        )
        
        if conta:

            quantidade = sincronizar_reunioes(
                conta,
                reunioes
            )

            print(
                f"💾 Reuniões sincronizadas no banco: "
                f"{quantidade}"
            )

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

    finally:

        if mail:

            try:

                mail.logout()

            except Exception:

                pass

