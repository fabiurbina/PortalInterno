from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
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
    salvar_inspecao,
    teste_socket,
    password_reset_view,
    criar_acesso_cliente,
    indicadores_view,
    analise_comercial,
    analise_producao,
    posicao_estoque_view,
    exportar_posicao_estoque_excel,
    relatorios_diversos,
    previsao_demanda,
    exportar_previsao_demanda_excel,
    controle_peso,
    qualidade_controle,
    chao_fabrica,
    atualizar_ordem_chao_fabrica,
    relatorio_lote_validade,
    exportar_lote_validade_excel,
    relatorio_classificacao_cliente,
    exportar_classificacao_cliente_excel
)

urlpatterns = [
    path('', dashboard, name='dashboard'),

    path('op/', home, name='home'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path(
        "esqueci-senha/",
        password_reset_view,
        name="password_reset",
    ),

    path(
        "esqueci-senha/enviado/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html",
        ),
        name="password_reset_done",
    ),

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
    name="salvar_inspecao",
    
),
    
    path("teste-socket/", teste_socket, name="teste_socket"),
    
    
    path(
    "portal/clientes/",
    criar_acesso_cliente,
    name="criar_acesso_cliente",
    
    
),
    
    path(
    "alterar-senha/",
        auth_views.PasswordChangeView.as_view(
            template_name="alterar_senha.html",
            success_url=reverse_lazy("dashboard"),
        ),
        name="password_change",
    ),
    
    path(
    "indicadores/",
    indicadores_view,
    name="indicadores"
),
    path(
    "analise-comercial/",
    analise_comercial,
    name="analise_comercial"
),
    
    path(
        "analise-producao/",
        analise_producao,
        name="analise_producao"
    ),
    
        path(
        
        "relatorios/",
            relatorios_diversos,
        name="relatorios_diversos"),

        
        path(
        "relatorios/posicao-estoque/",
            posicao_estoque_view,
        name="posicao_estoque"
    ),

    path(
        "relatorios/posicao-estoque/excel/",
            exportar_posicao_estoque_excel,
        name="exportar_posicao_estoque_excel"
    ),


    path(
        "relatorios/previsao-demanda/",
        previsao_demanda,
        name="previsao_demanda"
    ),
    
    
    path(
    "relatorios/previsao-demanda/exportar/",
    exportar_previsao_demanda_excel,
    name="exportar_previsao_demanda_excel",
    ),
    
    
    path(
    "relatorios/chao-fabrica/",
    chao_fabrica,
    name="chao_fabrica"
        ),
    
    
    path(
    "relatorios/chao-fabrica/atualizar-ordem/",
    atualizar_ordem_chao_fabrica,
    name="atualizar_ordem_chao_fabrica"
),
    
    
    
    path(
    "qualidade/controle/",
    qualidade_controle,
    name="qualidade_controle"
),
    
    path(
    "qualidade/controle-peso/",
    controle_peso,
    name="controle_peso"
),
    
     path(
        "relatorio/lote-validade/",
        relatorio_lote_validade,
        name="relatorio_lote_validade"
    ),
     
     path(
    "relatorio/lote-validade/exportar/",
        exportar_lote_validade_excel,
    name="exportar_lote_validade_excel"
    
),
     
     path(
    "relatorios/classificacao-cliente/",
        relatorio_classificacao_cliente,
    name="relatorio_classificacao_cliente"
),
     
     path(
    "relatorios/classificacao-cliente/exportar/",
    exportar_classificacao_cliente_excel,
    name="exportar_classificacao_cliente_excel"
),


]


