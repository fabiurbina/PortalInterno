from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .omie_service import (listar_ops, consultar_produto,consultar_op,listar_locais_estoque,
consultar_pedido, extrair_numero_pedido, listar_lotes,listar_quarentena, listar_movimentos_entrada)
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .mysql_service import (
    salvar_conferencia_mysql,
    consultar_conferencias,
    salvar_observacao_op,
    salvar_apontamento,
    consultar_apontamentos
)
from django.core.cache import cache




@login_required
def dashboard(request):

    return render(
        request,
        'dashboard.html'
    )
    
    
def home(request):

    ops = []

    ETAPAS = {
        "10": "Planejamento",
        "20": "Pesagem",
        "30": "Mistura",
        "40": "Encapsulamento",
        "50": "Envase",
        "60": "Concluído"
    }

    if request.method == 'POST':

        ultima_consulta = request.session.get('ultima_consulta')

        agora = timezone.now().timestamp()

        if ultima_consulta and (agora - ultima_consulta) < 3:

            messages.warning(
                request,
                'Aguarde 3 segundos antes de realizar uma nova consulta.'
            )

            return render(
                request,
                'home.html',
                {'ops': []}
            )

        request.session['ultima_consulta'] = agora

        etapa_filtro = request.POST.get('etapa')

        retorno = listar_ops()

        ops = retorno.get('cadastros', [])

        # adiciona o nome da etapa em todas as OPs
        produtos_cache = {}

        for op in ops:

            codigo = op['infAdicionais']['cEtapa']

            op['nome_etapa'] = ETAPAS.get(
                codigo,
                f"Etapa {codigo}"
            )

            cod_produto = op['identificacao']['nCodProduto']

            if cod_produto not in produtos_cache:

                produto = consultar_produto(cod_produto)

                produtos_cache[cod_produto] = produto.get(
                    'descricao',
                    str(cod_produto)
                )

            op['nome_produto'] = produtos_cache[cod_produto]

        # aplica o filtro se selecionado
        if etapa_filtro:

            ops = [
                op for op in ops
                if op['infAdicionais']['cEtapa'] == etapa_filtro
            ]

    return render(
        request,
        'home.html',
        {
            'ops': ops
        }
    )

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')


def ficha_op(request, codigo_op):

    op = consultar_op(codigo_op)
    
    if 'identificacao' not in op:

        return render(
            request,
            'ficha_op.html',
            {
                'erro': op.get(
                    'faultstring',
                    'Erro ao consultar OP'
                )
            }
        )

    # Busca descrição das matérias-primas
    produtos_cache = {}

    for item in op.get('itensDetalhes', []):

        codigo = item['nIdProdutoMalha']

        if codigo not in produtos_cache:

            produto_mp = consultar_produto(codigo)

            produtos_cache[codigo] = {
            'codigo': produto_mp.get('codigo', str(codigo)),
            'descricao': produto_mp.get('descricao', '')}

        item['codigo_produto'] = produtos_cache[codigo]['codigo']
        item['descricao_produto'] = produtos_cache[codigo]['descricao']

            
    locais = cache.get('locais_estoque')

    if not locais:

        locais = listar_locais_estoque()

        cache.set(
            'locais_estoque',
            locais,
            300
        )


    lotes = cache.get('lotes_omie')

    if not lotes:

        lotes = listar_lotes()

        cache.set(
            'lotes_omie',
            lotes,
            300
        )

    # Mapa de locais
    mapa_locais = {}

    for local in locais.get('locaisEncontrados', []):

        mapa_locais[
            local['codigo_local_estoque']
        ] = local['descricao']


    # Mapa de lotes
    mapa_lotes = {}
    
    

    for produto_lote in lotes.get('listaLotes', []):

        codigo_produto = produto_lote['ident']['nCodProd']

        if produto_lote.get('lotes'):

            lote = produto_lote['lotes'][0]

            mapa_lotes[codigo_produto] = {
                'lote': lote.get('cNumLote', ''),
                'validade': lote.get('dDataValidade', '')
            }

        else:

            mapa_lotes[codigo_produto] = {
                'lote': '',
                'validade': ''
            }
            
    #print(mapa_lotes)
    # Adiciona descrição do local + lote + validade
    for item in op.get('itensDetalhes', []):

        item['descricao_local'] = mapa_locais.get(
            item['codigo_local_estoque'],
            str(item['codigo_local_estoque'])
        )

        codigo = item['nIdProdutoMalha']

        item['lote'] = mapa_lotes.get(
            codigo,
            {}
        ).get(
            'lote',
            ''
        )

        item['validade'] = mapa_lotes.get(
            codigo,
            {}
        ).get(
            'validade',
            ''
        )
        

    mapa_locais = {}

    for local in locais.get('locaisEncontrados', []):

        mapa_locais[
            local['codigo_local_estoque']
        ] = local['descricao']


    for item in op.get('itensDetalhes', []):

        item['descricao_local'] = mapa_locais.get(
            item['codigo_local_estoque'],
            str(item['codigo_local_estoque'])
        )
        
        
    materias_primas = []
    embalagens = []

    for item in op.get('itensDetalhes', []):

        if item['descricao_local'] == 'Estoque Matéria Prima':
            materias_primas.append(item)

        elif item['descricao_local'] == 'Estoque de Embalagens':
            embalagens.append(item)
            

    produto = consultar_produto(
    op['identificacao']['nCodProduto']
    )

    codigo_pa = op['identificacao']['nCodProduto']
    
    codigo_op = op['identificacao']['cNumOP']

    conferencias = consultar_conferencias(
        codigo_op
    )
    
    apontamentos = consultar_apontamentos(
    codigo_op)
    
    #print(apontamentos)
    
    mapa_apontamentos = {}

    for apontamento in apontamentos:

        mapa_apontamentos[
            apontamento['etapa']
        ] = apontamento

    mapa_conferencias = {}

    for conferencia in conferencias:

        mapa_conferencias[
            str(conferencia['codigo_produto'])
        ] = conferencia

    for item in op.get('itensDetalhes', []):
        

        item['conferido'] = (
            str(int(item['codigo_produto']))
            in mapa_conferencias
        )

    # Lote do Produto Acabado
    lote_pa = mapa_lotes.get(
        codigo_pa,
        {}
    ).get(
        'lote',
        ''
    )

    validade_pa = mapa_lotes.get(
        codigo_pa,
        {}
    ).get(
        'validade',
        ''
    )

    obs = op['observacoes']['cObs']

    #numero_pedido = extrair_numero_pedido(obs)

    #pedido = None

    #if numero_pedido:
        #pedido = consultar_pedido(numero_pedido)

    nome_produto = produto.get(
        'descricao',
        op['identificacao']['nCodProduto']
    )

    ETAPAS = {
        "10": "Planejamento",
        "20": "Pesagem",
        "30": "Mistura",
        "40": "Encapsulamento",
        "50": "Envase",
        "60": "Concluído"
    }

    nome_etapa = ETAPAS.get(
        op['infAdicionais']['cEtapa'],
        op['infAdicionais']['cEtapa']
    )
    
    ETAPAS_PRODUCAO = [
        "FRACIONAMENTO",
        "MISTURA",
        "ENVASE",
        "EXPEDICAO"
    ]

    return render(
        request,
        'ficha_op.html',
        {
            'op': op,
            'nome_produto': nome_produto,
            'nome_etapa': nome_etapa,
            'materias_primas': materias_primas,
            'embalagens': embalagens,
            'pedido': None,
            'numero_pedido': None,
            'lote_pa': lote_pa,
            'validade_pa': validade_pa,
            'etapas_producao': ETAPAS_PRODUCAO,
            'apontamentos': mapa_apontamentos,
        }
    )

@csrf_exempt
def salvar_conferencia(request):

    if request.method == "POST":

        dados = json.loads(request.body)
        
        from datetime import datetime

        validade = None

        if dados['validade']:
            validade = datetime.strptime(
                dados['validade'],
                '%d/%m/%Y'
            ).date()
            
        validade_pa = None

        if dados['validade_pa']:
            validade_pa = datetime.strptime(
                dados['validade_pa'],
                '%d/%m/%Y'
            ).date()

        salvar_conferencia_mysql(
            codigo_op=dados['op'],
            codigo_produto=dados['produto'],
            descricao_produto=dados['descricao'],
            tipo=dados['tipo'],
            lote=dados['lote'],
            validade=validade,
            conferido=dados['conferido'],
            usuario=request.user.username,
            lote_pa = dados['lote_pa'],
            validade_pa = validade_pa,
            observacao = dados.get('observacao',''),
            limpeza_sala=dados.get('limpeza_sala'),
            limpeza_equipamento=dados.get('limpeza_equipamento')
            
        )

        print("Conferência salva!")

        return JsonResponse({
            "sucesso": True
        })

    return JsonResponse({
        "sucesso": False
    })
    
@csrf_exempt
def salvar_observacao(request):

    if request.method == "POST":

        dados = json.loads(request.body)

        salvar_observacao_op(
            codigo_op=dados['op'],
            observacao=dados['observacao'],
            usuario=request.user.username
        )

        return JsonResponse({
            "sucesso": True
        })

    return JsonResponse({
        "sucesso": False
    })
    

@csrf_exempt
def salvar_apontamento_view(request):
    
    try:

        if request.method == "POST":

            dados = json.loads(
                request.body
            )

            salvar_apontamento(
                codigo_op=dados['op'],
                etapa=dados['etapa'],
                data_inicio=dados['inicio'],
                data_fim=dados['fim'],
                peso=dados['peso'],
                usuario=request.user.username
            )

            return JsonResponse({
                    "sucesso": True
                })

    except Exception as e:

        print("ERRO APONTAMENTO:")
        print(e)

        return JsonResponse({
            "sucesso": False,
            "erro": str(e)
        })

    return JsonResponse({
        "sucesso": False
    })
    
    
def qualidade_home(request):

    return render(
        request,
        'qualidade_home.html'
    )
    


@login_required
def qualidade_home(request):

    data_inicial = request.GET.get(
        'data_inicial'
    )

    data_final = request.GET.get(
        'data_final'
    )

    entradas = []

    if data_inicial and data_final:

        data_inicial = (
            data_inicial
            .split('-')
        )

        data_final = (
            data_final
            .split('-')
        )

        data_inicial = (
            f"{data_inicial[2]}/"
            f"{data_inicial[1]}/"
            f"{data_inicial[0]}"
        )

        data_final = (
            f"{data_final[2]}/"
            f"{data_final[1]}/"
            f"{data_final[0]}"
        )

        entradas = listar_movimentos_entrada(
            data_inicial,
            data_final
        )

    return render(
        request,
        'qualidade_home.html',
        {
            'entradas': entradas
        }
    )