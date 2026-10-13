from django.urls import path

from .views import (
    dashboard,
    login_view,
    logout_view,
    indicadores_comercial_dados,
)

urlpatterns = [
    # Login
    path("login/", login_view, name="login"),

    # Painel principal dos sócios
    path("", dashboard, name="dashboard"),

    # Encerrar sessão
    path("logout/", logout_view, name="logout"),

    # Dados dos indicadores comerciais
    path(
        "indicadores/comercial/dados/",
        indicadores_comercial_dados,
        name="indicadores_comercial_dados",
    ),
]
