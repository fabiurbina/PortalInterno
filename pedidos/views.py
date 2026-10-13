
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import (
    login_required,
    login_not_required,
)
from django.http import JsonResponse
from django.db import connection


def usuario_eh_socio(usuario):
    if not usuario.is_authenticated:
        return False

    if usuario.is_superuser:
        return True

    return usuario.groups.filter(
        name__in=["Socios", "Sócios"]
    ).exists()


@login_not_required
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    erro = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        usuario = authenticate(
            request,
            username=username,
            password=password,
        )

        if usuario is not None:
            login(request, usuario)
            return redirect("dashboard")

        erro = "Usuário ou senha inválidos."

    return render(
        request,
        "login.html",
        {"erro": erro},
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    if not usuario_eh_socio(request.user):
        return render(
            request,
            "acesso_negado.html",
            status=403,
        )

    return render(request, "dashboard.html")


@login_required
def indicadores_comercial_dados(request):
    if not usuario_eh_socio(request.user):
        return JsonResponse(
            {"erro": "Acesso não autorizado."},
            status=403,
        )

    sql = """
        SELECT *
        FROM ViesanoDW.vw_ia_comercial
    """

    with connection.cursor() as cursor:
        cursor.execute(sql)

        colunas = [
            coluna[0]
            for coluna in cursor.description
        ]

        registros = [
            dict(zip(colunas, linha))
            for linha in cursor.fetchall()
        ]

    total_oportunidades = len(registros)

    total_ativos = sum(
        1 for r in registros
        if r.get("status") == "Ativo"
    )

    total_conquistados = sum(
        1 for r in registros
        if r.get("status") == "Conquistado"
    )

    total_suspensos = sum(
        1 for r in registros
        if r.get("status") == "Suspenso"
    )

    total_cancelados = sum(
        1 for r in registros
        if r.get("status") == "Cancelado"
    )

    valor_pipeline = sum(
        float(r.get("valor") or 0)
        for r in registros
        if r.get("status") == "Ativo"
    )

    valor_conquistado = sum(
        float(r.get("valor") or 0)
        for r in registros
        if r.get("status") == "Conquistado"
    )

    taxa_conversao = (
        total_conquistados / total_oportunidades * 100
        if total_oportunidades else 0
    )

    base_absorcao = valor_pipeline + valor_conquistado

    absorcao_pipeline = (
        valor_conquistado / base_absorcao * 100
        if base_absorcao else 0
    )

    tempos_negociacao = [
        float(r["DiasNoPipeline"])
        for r in registros
        if r.get("DiasNoPipeline") is not None
        and r.get("DataConclusao") is not None
    ]

    tempo_medio_negociacao = (
        round(
            sum(tempos_negociacao)
            / len(tempos_negociacao)
        )
        if tempos_negociacao else 0
    )

    return JsonResponse({
        "total_oportunidades": total_oportunidades,
        "total_ativos": total_ativos,
        "total_conquistados": total_conquistados,
        "total_suspensos": total_suspensos,
        "total_cancelados": total_cancelados,
        "valor_pipeline": round(valor_pipeline, 2),
        "valor_conquistado": round(valor_conquistado, 2),
        "taxa_conversao": round(taxa_conversao, 2),
        "absorcao_pipeline": round(absorcao_pipeline, 2),
        "tempo_medio_negociacao": tempo_medio_negociacao,
    })
