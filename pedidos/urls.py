from django.urls import path
from .views import (
    dashboard,
    home,
    login_view,
    logout_view,
    ficha_op,
    salvar_conferencia,
    salvar_observacao,
    salvar_apontamento_view,
    qualidade_home
)

urlpatterns = [
    path('', dashboard, name='dashboard'),

    path('op/', home, name='home'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path(
        'ficha/<int:codigo_op>/',
        ficha_op,
        name='ficha_op'
    ),

    path(
        'salvar-conferencia/',
        salvar_conferencia,
        name='salvar_conferencia'
    ),

    path(
        'salvar-observacao/',
        salvar_observacao,
        name='salvar_observacao'
    ),
    
    path(
    'salvar-apontamento/',
    salvar_apontamento_view,
    name='salvar_apontamento'
),
    path(
    'qualidade/',
    qualidade_home,
    name='qualidade_home'
),
]


