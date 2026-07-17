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
    teste_socket

)

urlpatterns = [
    path('', dashboard, name='dashboard'),

    path('op/', home, name='home'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path(
    "esqueci-senha/",
    auth_views.PasswordResetView.as_view(
        template_name="password_reset.html",
        email_template_name="emails/password_reset_email.html",
        subject_template_name="emails/password_reset_subject.txt",
        success_url=reverse_lazy("password_reset_done"),
    ),
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
        "redefinir/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),

    path(
        "redefinir/concluido/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html",
        ),
        name="password_reset_complete",
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
]
