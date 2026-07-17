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
    qualidade_home,
    estoque_home,
    ficha_logistica,
    qualidade_inspecao,
    pedidos,
    relatorio_mrp_view,
    exportar_mrp_excel,
    salvar_inspecao
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
    
    path(
    "qualidade/inspecao/<int:cod_prod>/",   
    qualidade_inspecao,
    name="qualidade_inspecao",
),
    
    path(
    'estoque/',
    estoque_home,
    name='estoque_home'
),
    
    path(
    'logistica/<int:codigo_op>/',
    ficha_logistica,
    name='ficha_logistica'
),
    
    path(
    "pedidos/",
    pedidos,
    name="pedidos"
),
    
    path(
    "relatorios/mrp/",
    relatorio_mrp_view,
    name="relatorio_mrp"
),
    
    path(
    "relatorios/mrp/exportar/",
    exportar_mrp_excel,
    name="exportar_mrp_excel"
),
    
    path(
    "qualidade/salvar/",
    salvar_inspecao,
    name="salvar_inspecao"
),

]
